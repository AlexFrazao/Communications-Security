import json
import subprocess
import time

# terminal command: zokrates compute-witness --abi --stdin < input.json

fleet = [
    [0, 0], [1, 0], [2, 0], [3, 0], [4, 0],
    [0, 1], [1, 1], [2, 1], [3, 1],
    [0, 2], [1, 2], [2, 2],
    [0, 3], [1, 3],
    [0, 4], [1, 4],
    [0, 5],
    [0, 6]
    ]

nonce = 5

shot = [9, 9]

def create_input_for_proof2(shot, fleet, nonce):
    file = open('../proof_1/proof.json')
    content = json.load(file)
    file.close()

    data = [
        [str(number) for number in shot],
        [[str(number) for number in group] for group in fleet],
        str(nonce),
        content['inputs']
    ]

    with open('input.json', 'w+') as output_file:
        json.dump(data, output_file)

def run_proof2():
    with open('input.json', 'r') as infile:
        subprocess.run(['zokrates', 'compute-witness', '--abi', '--stdin'], stdin=infile) # , stdout=sys.stdout, stderr=sys.stderr

    time.sleep(2)

create_input_for_proof2(shot, fleet, nonce)
run_proof2()