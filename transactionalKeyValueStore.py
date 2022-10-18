class KVStore:
    def __init__(self):
        self.globalStore = {}
        # TransactionStack maintains a list of active transactions
        self.TransactionStack = [] # [{ ....},{....}]
        self.open_trans = 0

    def get(self,key):
        return self.globalStore[key]
    
    def begin(self):
        self.open_trans += 1
        activeTrans = {}
        self.TransactionStack.append(activeTrans)

    def set(self,key: Any, value: Any):
        # whether any active/open transactions present ?
        # If none, we are going to update the Global Store
        if self.open_trans == 0:
            self.globalStore[key] = value
            return
        # Active transaction
        activeTrans = self.TransactionStack[-1]
        activeTrans[key] = value
        
    def commit(self):
        # check whether any open transactions to commit
        # If no open/active transactions, nothing to commit; so return
        if self.open_trans == 0:
            return
        
        activeTrans = self.TransactionStack[-1]
        # update the changes in globalStore
        self.globalStore.update(activeTrans)
        # delete the committed transaction
        self.TransactionStack.pop()
        # update the open_trans count
        self.open_trans -= 1

    def rollback(self):
        # check whether any open transactions to commit
        if self.open_trans == 0:
            return
        self.TransactionStack.pop()
        # update the open_trans
        self.open_trans -= 1

kv = KVStore()
print(kv)
kv.begin()
kv.set(1,10)
kv.set(2,20)
kv.set(1,4)
kv.commit()
kv.rollback()
kv.begin()
kv.set(1, 5)
kv.set(2, 6)
kv.commit()

kv.rollback()
kv.commit()
