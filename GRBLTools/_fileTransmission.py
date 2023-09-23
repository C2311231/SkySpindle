import time

def SendFile(self, filePath, mode, buffer):
        self.status = 'Operating'
        file = open(filePath, 'r')
        file = file.readlines()
        self.linenum = 1
        self.operationStartTime = time.time()
        self.KILLOPERATION = False
                
        if mode == 'Reliable':
            self.notSending = False
            self.requested = 0
            self.okCount = 0
            for line in file:
                self.notSending = False
                l = line.strip() # Strip all EOL characters for consistency
                buffer.append(["FileCommand", (l + f' N{self.linenum}\n').encode()]) # Send g-code block to grbl
                self.requested += 1
                while self.requested > self.okCount:
                    if self.KILLOPERATION:
                        return
                    self.notSending = True
                    completion =  (self.linenum/self.fileLenght)*100
                    self.OperationETA = (100-completion)*((time.time() - self.operationStartTime)/completion)
                    time.sleep(0.3)
                self.linenum += 1
                self.SocketEmit('lineNum', [self.linenum, self.fileLenght])
        self.status = 'Idle'