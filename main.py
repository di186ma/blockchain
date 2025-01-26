import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", 0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            timestamp=time.time(),
            data=data,
            proof=self.proof_of_work(latest_block.proof)
        )
        self.chain.append(new_block)

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.is_valid_proof(last_proof, proof):
            proof += 1
        return proof

    def is_valid_proof(self, last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not self.is_valid_proof(previous_block.proof, current_block.proof):
                return False

        return True

# Пример использования
if __name__ == "__main__":
    blockchain = Blockchain()

    print("Генерация блоков...")
    blockchain.add_block("Перевод 1 монеты от Alice к Bob")
    blockchain.add_block("Перевод 2 монет от Bob к Charlie")

    for block in blockchain.chain:
        print(f"Блок {block.index}:\n"
              f"Хэш: {block.hash}\n"
              f"Данные: {block.data}\n"
              f"Предыдущий хэш: {block.previous_hash}\n"
              f"Время: {time.ctime(block.timestamp)}\n"
              f"Proof: {block.proof}\n")

    print(f"Цепочка валидна? {blockchain.is_chain_valid()}")
