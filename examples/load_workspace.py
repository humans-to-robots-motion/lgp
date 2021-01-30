import sys
import argparse
import yaml
from os.path import join, dirname, abspath

ROOT_DIR = join(dirname(abspath(__file__)), '..')
DATA_DIR = join(ROOT_DIR, 'data', 'scenarios')
sys.path.append(ROOT_DIR)
from lgp.geometry.workspace import LGPWorkspace  # noqa

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Example run: python load_workspace.py prepare_meal.yaml')
parser.add_argument('yaml_file', help='The world URDF file', type=str)
args = parser.parse_args()

with open(join(DATA_DIR, args.yaml_file), 'r') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

workspace = LGPWorkspace(config)
workspace.draw_kinematic_tree()