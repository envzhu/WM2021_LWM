"""
LBF(M)モデル
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

"""
Encoder
入力：潜在変数zとメッセージmのそれぞれの系列
出力：潜在信念変数betaの平均値と標準偏差
"""
class BetaEncoder(nn.Module):
    """ LBF encoder """
    def __init__(self, z_dim):
        super(Encoder, self).__init__()
        self.z_dim = z_dim
        self.rnn_hidden_size = 128

        self.rnn = nn.RNN(m_dim+z_dim, self.rnn_hidden_size, 1, bacth_first=True)
        self.fc1 = nn.Linear(self.rnn_hidden_size, 1024)
        self.fc_mean = nn.Linear(1024, beta_dim)
        self.fc_logstd = nn.Linear(1024, beta_dim)

    def forward(self, m_seq, z_seq):
        # [B_SIZE, SEQ_LEN, m_dim+z_dim]
        x = F.relu(self.fc1(torch.cat([m, z], dim=1))
        x = F.relu(self.fc2(x)) 

        mean = self.fc_mean(x)
        logstd = self.fc_logstd(x)

        return mean, logstd


"""
Decoder
入力：潜在変数beta_t
出力：予測 [z_t, .., z_{t+pred_z_steps-1}]
"""
class ZSeqDecoder(nn.Module):
    """ LBF decoder """
    def __init__(self, beta_dim, z_dim, pred_z_steps):
        super(Decoder, self).__init__()
        self.beta_dim = beta_dim
        self.z_dim = z_dim
        self.pred_z_steps = pred_z_steps

        self.fc1 = nn.Linear(beta_dim, 1024)
        self.fc2 = nn.Linear(1024, pred_z_steps*z_dim)

    def forward(self, beta):
        # [B_SIZE, SEQ_LEN, beta_dim]
        x = F.relu(self.fc1(beta)) # [B_SIZE, SEQ_LEN, 1024]
        prediction = self.fc2(x)   # [B_SIZE, SEQ_LEN, pred_z_steps*z_dim]  最終層は活性化関数を適用しない
    `   prediction = prediction.view(-1, -1, self.pred_z_steps, self.z_dim) # [B_SIZE, SEQ_LEN, pred_z_steps, z_dim]
        return prediction


class LBF(nn.Module):
    def __init__(self, beta_dim, m_dim, z_dim, pred_z_steps):
        super(LBF, self).__init__()
        self.encoder = BetaEncoder(beta_dim, m_dim, z_dim)
        self.decoder = ZSeqDecoder(beta_dim, z_dim, pred_z_steps)
      
    def sample_beta(self, mean, logstd):
        # 再パラメータ化トリック
        epsilon = torch.randn_like(mean)
        return mean + logstd.exp() * epsilon

    def forward(self, m_seq, z_seq):
        beta_mean, beta_logstd = self.encoder(m, z)
        beta = self.sample_beta(beta_mean, beta_logstd)

        pred_zs = self.decoder(beta)
        return pred_zs, beta, beta_mean, beta_logstd

    def loss(self, real_zs, pred_zs, beta_mean, beta_logstd):
        # betaの分布と正規分布間のKLダイバージェンス
        KL_loss = -0.5 * torch.sum(1 + 2*beta_logstd - beta_mean**2 - (2*beta_logstd).exp()) / beta_mean.shape[0]

        # 予測誤差
        pred_loss = F.mse_loss(real_zs, pred_zs, reduction='mean')
        return KL_loss+pred_loss, KL_loss, pred_loss
