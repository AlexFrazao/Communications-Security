import json

proof1_zok = """
import "hashes/sha256/sha256Padded";

def main(private u8 [18][2] fleet, private u8 nonce) -> u32 [8] {
    for u32 i in 0..18 {
        bool out_of_bounds = \
        if fleet[i][0] < 0 || \
        fleet[i][0] > 9 || \
        fleet[i][1] < 0 || \
        fleet[i][1] > 9 {false} \
        else {true};
        assert(out_of_bounds);
        for u32 j in 0..18 {
            bool collision = \
            if fleet[i] == fleet[j] && \
            i != j {false} \
            else {true};
            assert(collision);
        }
    }
    
    u32[8] hash = sha256Padded(\
    [fleet[0][0], fleet[0][1], fleet[1][0], fleet[1][1],\
    fleet[2][0], fleet[2][1], fleet[3][0], fleet[3][1],\
    fleet[4][0], fleet[4][1], fleet[5][0], fleet[5][1],\
    fleet[6][0], fleet[6][1], fleet[7][0], fleet[7][1],\
    fleet[8][0], fleet[8][1], fleet[9][0], fleet[9][1],\
    fleet[10][0], fleet[10][1], fleet[11][0], fleet[11][1],\
    fleet[12][0], fleet[12][1], fleet[13][0], fleet[13][1],\
    fleet[14][0], fleet[14][1], fleet[15][0], fleet[15][1],\
    fleet[16][0], fleet[16][1], fleet[17][0], fleet[17][1],\
    nonce]);

    return hash;
}
"""

proof2_zok = """
import "hashes/sha256/sha256Padded";

def main(private u8 [2] shot, private u8 [18][2] mut fleet, private u8 nonce, u32 [8] old_hash) -> u32 [8] {
    u32[8] check_hash = sha256Padded(\
    [fleet[0][0], fleet[0][1], fleet[1][0], fleet[1][1],\
    fleet[2][0], fleet[2][1], fleet[3][0], fleet[3][1],\
    fleet[4][0], fleet[4][1], fleet[5][0], fleet[5][1],\
    fleet[6][0], fleet[6][1], fleet[7][0], fleet[7][1],\
    fleet[8][0], fleet[8][1], fleet[9][0], fleet[9][1],\
    fleet[10][0], fleet[10][1], fleet[11][0], fleet[11][1],\
    fleet[12][0], fleet[12][1], fleet[13][0], fleet[13][1],\
    fleet[14][0], fleet[14][1], fleet[15][0], fleet[15][1],\
    fleet[16][0], fleet[16][1], fleet[17][0], fleet[17][1],\
    nonce]);
    assert(check_hash == old_hash);

    for u32 i in 0..18 {
        fleet[i] = \
        if shot != fleet[i] {fleet[i]} else {[11, 11]};
    }
    
    u32 [8] hash = \
    sha256Padded(\
    [fleet[0][0], fleet[0][1], fleet[1][0], fleet[1][1],\
    fleet[2][0], fleet[2][1], fleet[3][0], fleet[3][1],\
    fleet[4][0], fleet[4][1], fleet[5][0], fleet[5][1],\
    fleet[6][0], fleet[6][1], fleet[7][0], fleet[7][1],\
    fleet[8][0], fleet[8][1], fleet[9][0], fleet[9][1],\
    fleet[10][0], fleet[10][1], fleet[11][0], fleet[11][1],\
    fleet[12][0], fleet[12][1], fleet[13][0], fleet[13][1],\
    fleet[14][0], fleet[14][1], fleet[15][0], fleet[15][1],\
    fleet[16][0], fleet[16][1], fleet[17][0], fleet[17][1],\
    nonce]);

    return hash;
}
"""

proof3_zok = """
def main(private u8 [18][2] fleet) -> field {
    field mut remaining = 18;
    
    for u32 i in 0..18 {
        remaining = remaining - \
        (fleet[i] == [11, 11] ? 1 : 0);
    }
    // assert(remaining > 0);
    return remaining;
}
"""

# Mapping of proof names to their corresponding data
proofs = {
    "proof1_zok": proof1_zok,
    "proof2_zok": proof2_zok,
    "proof3_zok": proof3_zok
}

def process_proof(proof_request):
    proof_name = proof_request.get("proof_name")
    proof_data = proofs.get(proof_name, "Invalid proof name")
    proof_result = {"status": "success", "proof": proof_data} if proof_name in proofs else {"status": "failure", "error": "Invalid proof name"}
    return proof_result

def proof_main(proof_request_str):
    proof_request = json.loads(proof_request_str)
    proof_result = process_proof(proof_request)
    return json.dumps(proof_result)
