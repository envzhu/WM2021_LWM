import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser("Experiments in Language World Model")
    # Core training parameters
    parser.add_argument("--lr", type=float, default=5e-3, help="learning rate for Adam optimizer")
    parser.add_argument("--batch_size", type=int, default=64, help="batch size")
    parser.add_argument("--m_dim", type=int, default=64, help="m dim")
    parser.add_argument("--z_dim", type=int, default=64, help="z dim")
    parser.add_argument("--num_episodes", type=int, default=200000, help="number of episodes")
    # Checkpointing, logging and saving
    #parser.add_argument("--verbose", action="store_true", default=False, help="prints out more info during training")
    parser.add_argument("--seed", type=int, default=0, help="random seed")
    parser.add_argument("--print_freq", type=int, default=100, help="how frequently log is printed")
    parser.add_argument("--save_freq", type=int, default=None, help="how frequently model is saved")
    parser.add_argument("--test_freq", type=int, default=100, help="how frequently model is tested")
    parser.add_argument("--checkpoints_dir", type=str, default="./checkpoints/", help="directory where model and results are saved")
    parser.add_argument("--load_dir", type=str, default=None, help="directory where model is loaded from")
    parser.add_argument('--results_dir', type=str, default='./results/', help='directory where results are saved.')

    parser.add_argument("--exp-name", type=str, default=None, help="save name")

    args = parser.parse_args()

    args.save_freq = args.num_episodes if args.save_freq is None else args.save_freq

    os.makedirs(args.checkpoints_dir, exist_ok=True)
    os.makedirs(args.results_dir, exist_ok=True)

    return args
