import json
import subprocess
import sys
import time

# Function to compute witness for proof1
def compute_witness_proof1(fleet, nonce, player_directory):
    data = [
        [[str(number) for number in group] for group in fleet],
        str(nonce)
    ]

    with open(f'{player_directory}/proof1/input.json', 'w+') as output_file:
        json.dump(data, output_file)

def run_proof1(player_directory):
    with open(f'{player_directory}/proof1/input.json', 'r') as infile:
        subprocess.run(['zokrates', 'compute-witness', '--abi', '--stdin'], stdin=infile, cwd=f'{player_directory}/proof1')

def get_hash_from_file(player_directory):
    file = open(f"{player_directory}/hash.json")
    content = json.load(file)
    file.close()
    return content

# Function to compute witness for proof2
def create_input_for_proof2(shot, fleet, nonce, player_directory):
    with open(f'{player_directory}/proof1/proof.json') as file:
        content = json.load(file)

    data = [
        [str(number) for number in shot],
        [[str(number) for number in group] for group in fleet],
        str(nonce),
        get_hash_from_file(player_directory)#content['inputs']
    ]

    with open(f'{player_directory}/proof2/input.json', 'w+') as output_file:
        json.dump(data, output_file)

def run_proof2(player_directory):
    with open(f'{player_directory}/proof2/input.json', 'r') as infile:
        subprocess.run(['zokrates', 'compute-witness', '--abi', '--stdin'], stdin=infile, cwd=f'{player_directory}/proof2')

# Function to compute witness for proof3
def create_input_for_proof3(fleet, player_directory):
    data = [
        [[str(number) for number in group] for group in fleet]
    ]

    with open(f'{player_directory}/proof3/input.json', 'w+') as output_file:
        json.dump(data, output_file)

def run_proof3(player_directory):
    with open(f'{player_directory}/proof3/input.json', 'r') as infile:
        subprocess.run(['zokrates', 'compute-witness', '--abi', '--stdin'], stdin=infile, cwd=f'{player_directory}/proof3')

# Main function to route to the correct proof computation
def main():
    if len(sys.argv) < 2:
        print("Usage: python compute_witness.py <proof_number> [additional arguments...]")
        sys.exit(1)

    proof_number = int(sys.argv[1])

    if proof_number == 1:
        if len(sys.argv) != 5:
            print("Usage for proof1: python compute_witness.py 1 <fleet> <nonce> <player_directory>")
            sys.exit(1)

        fleet = json.loads(sys.argv[2])
        nonce = int(sys.argv[3])
        player_directory = sys.argv[4]
        compute_witness_proof1(fleet, nonce, player_directory)
        run_proof1(player_directory)

    elif proof_number == 2:
        if len(sys.argv) != 6:
            print("Usage for proof2: python compute_witness.py 2 <shot> <fleet> <nonce> <player_directory>")
            sys.exit(1)

        shot = json.loads(sys.argv[2])
        fleet = json.loads(sys.argv[3])
        nonce = int(sys.argv[4])
        player_directory = sys.argv[5]
        create_input_for_proof2(shot, fleet, nonce, player_directory)
        run_proof2(player_directory)

    elif proof_number == 3:
        if len(sys.argv) != 4:
            print("Usage for proof3: python compute_witness.py 3 <fleet>")
            sys.exit(1)

        fleet = json.loads(sys.argv[2])
        player_directory = sys.argv[3]
        create_input_for_proof3(fleet, player_directory)
        run_proof3(player_directory)

    else:
        print(f"Invalid proof number: {proof_number}")
        sys.exit(1)

if __name__ == "__main__":
    main()
