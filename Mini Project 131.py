#Bank Account Simulation

from datetime import datetime

# ---------------- Transaction Class ----------------
class Transaction:
    def __init__(self, txn_type, amount, balance):
        self.txn_type = txn_type   # "deposit", "withdraw", "transfer"
        self.amount = amount
        self.balance = balance
        self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.txn_type.capitalize()}: ₹{self.amount:.2f} | Balance: ₹{self.balance:.2f}"


# ---------------- Base Account Class ----------------
class Account:
    def __init__(self, account_number, holder_name, initial_balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.__balance = initial_balance   # Encapsulation: private attribute
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.transactions.append(Transaction("deposit", amount, self.__balance))
            return True
        return False

    def withdraw(self, amount):
        """Base withdraw: may be overridden in subclasses"""
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            self.transactions.append(Transaction("withdraw", amount, self.__balance))
            return True
        return False

    def transfer(self, target_account, amount):
        if self.withdraw(amount):
            target_account.deposit(amount)
            self.transactions.append(Transaction("transfer", amount, self.__balance))
            return True
        return False

    def get_balance(self):
        return self.__balance   # controlled access to private variable

    def show_transactions(self):
        for txn in self.transactions:
            print(txn)

    def __str__(self):
        return f"Account[{self.account_number}] - {self.holder_name} | Balance: ₹{self.__balance:.2f}"


# ---------------- Savings Account ----------------
class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, initial_balance=0, withdraw_limit=20000):
        super().__init__(account_number, holder_name, initial_balance)
        self.withdraw_limit = withdraw_limit

    def withdraw(self, amount):
        """Override: Apply withdrawal limit"""
        if amount > self.withdraw_limit:
            print(f"❌ Withdrawal failed! Limit is ₹{self.withdraw_limit}")
            return False
        return super().withdraw(amount)


# ---------------- Current Account ----------------
class CurrentAccount(Account):
    def __init__(self, account_number, holder_name, initial_balance=0, overdraft_limit=10000):
        super().__init__(account_number, holder_name, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        """Override: Allow overdraft facility"""
        if amount > 0 and (self.get_balance() + self.overdraft_limit) >= amount:
            # Directly manipulate using deposit(-amount) for consistent txn
            return super().withdraw(amount) or self._overdraft_withdraw(amount)
        return False

    def _overdraft_withdraw(self, amount):
        # Overdraft case: manually adjust balance
        # Accessing parent private balance safely via transfer logic
        self._Account__balance -= amount
        self.transactions.append(Transaction("overdraft_withdraw", amount, self._Account__balance))
        return True


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    # Create accounts
    acc1 = SavingsAccount("S001", "Alice", 50000, withdraw_limit=20000)
    acc2 = CurrentAccount("C001", "Bob", 10000, overdraft_limit=15000)

    print(acc1)
    print(acc2)

    # Transactions
    acc1.deposit(5000)
    acc1.withdraw(25000)  # exceeds limit
    acc1.withdraw(15000)

    acc2.withdraw(20000)  # allowed due to overdraft
    acc2.deposit(5000)

    # Transfer
    acc1.transfer(acc2, 10000)

    # Show balances
    print("\nFinal Balances:")
    print(acc1)
    print(acc2)

    # Show transactions
    print("\nAlice Transactions:")
    acc1.show_transactions()

    print("\nBob Transactions:")
    acc2.show_transactions()
