import json
import subprocess
import time
import sys

def compute_witness_proof1(fleet, nonce, player_number):
    data = [
        [[str(number) for number in group] for group in fleet],
        str(nonce)
    ]

    with open(f'player_{player_number}/proof1/input.json', 'w+') as output_file:
        json.dump(data, output_file)

def run_proof1(player_number):
    with open(f'player_{player_number}/proof1/input.json', 'r') as infile:
        subprocess.run(['zokrates', 'compute-witness', '--abi', '--stdin'], stdin=infile, cwd=f'player_{player_number}/proof1')

if __name__ == "__main__":
    fleet = json.loads(sys.argv[1])
    nonce = int(sys.argv[2])
    player_number = sys.argv[3]

    compute_witness_proof1(fleet, nonce, player_number)
    run_proof1(player_number)
    time.sleep(2)