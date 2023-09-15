import time

def SendFile(self, filePath, mode, buffer):
        self.status = 'Operating'
        file = open(filePath, 'r')
        file = file.readlines()
        self.linenum = 1
        self.operationStartTime = time.time()
        self.KILLOPERATION = False
        # if mode == 'Fast':               # NONFUNCTIONAL
        #     linesCharactorCounts = []
        #     RX_BUFFER_SIZE = 100
        #     GCodeCount = 0
        #     linesInBuffer = 0
        #     for line in file:
        #         self.Async = False
        #         line = re.sub(r'\s|\(.*?\)', '', line).upper().strip()
        #         line = line +f'N{self.linenum}'
        #         linesCharactorCounts.append(len(line)+1)
        #         print(f'charactorcount = {sum(linesCharactorCounts)}')
        #         while sum(linesCharactorCounts) >= RX_BUFFER_SIZE - 1 or self.connection.in_waiting:
        #             returnData = self.connection.readline().decode()
        #             print('recived ' + returnData)
        #             returnData = returnData.strip()
        #             if 'error' in returnData:
        #                 print(f'GRBL Reports Error on line {self.linenum-linesInBuffer}:   {returnData}')
        #                 return
        #             elif 'echo' not in line:
        #                 GCodeCount +=1
        #                 linesInBuffer -= 1
        #                 if linesCharactorCounts:
        #                     del linesCharactorCounts[0]
                
        #         self.connection.write((line + '\n').encode())
        #         linesInBuffer += 1
        #         self.linenum += 1
                
                
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
                self.SocketEmit('LineNum', [self.linenum, self.fileLenght])
        self.status = 'Idle'