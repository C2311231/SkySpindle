import time

def GetData(self):
    self.Async = True
    while self.Async:
        line = self.connection.readline().decode().strip()
        if self.Async == False:
            break
        
        if line.startswith('<') and line.endswith('>'):
            StatusReportProcess(self, line)
            self.SocketEmit('console', {'data': line, 'class': 'status'})
            
        elif line.startswith('ok'):
            self.okCount += 1 
            self.SocketEmit('console', {'data': line, 'class': 'recive'})   
        
        elif line.startswith('$') and '=' in line:
            self.SocketEmit('console', {'data': line, 'class': 'recive'}) 
              
            if 'N' not in line:
                processGRBLSetting(self, line)
                
            else:
                data = line.replace('$N', '').split('=')
                self.startuplines[data[0]] = data[1]
            
        elif line.startswith('[') and line.endswith(']'):
            self.SocketEmit('console', {'data': line, 'class': 'recive'})  
             
            if 'MSG:' in line:
                print(f'GRBL sent a message: {line}')
                
            elif 'GC:' in line:
                self.GcodeParserState = line.replace(']', '').replace('[GC:', '').split(' ')
            
            elif 'VER:' in line:
                self.Version = line.replace(':]', '').replace('[VER:', '')
                
            elif 'OPT:' in line:
                self.OPT = line.replace(']', '').replace('[OPT:', '')
                
            elif 'echo:' in line:
                pass
            
            elif 'G54' in line or'G55' in line or'G56' in line or'G57' in line or'G58' in line or'G59' in line or'G28' in line or'G30' in line or'G92' in line or'TLO' in line or'PRB' in line:
                self.SP[line.split(':')[0].replace(':', '').replace('[', '')] = line.split(':')[1].replace(']', '').split(',')
                
        elif line.startswith('ALARM'):
            print(f'GRBL reports an alarm: {line}')
            self.SocketEmit('console', {'data': line, 'class': 'recive'})
            self.KILLOPERATION = True 
              
        elif line.startswith('>'):
            data = line.replace(">", '').split(':')
            if data[1] != 'ok':
                print(f'Start line failed {data[0]}')
            self.SocketEmit('console', {'data': line, 'class': 'recive'})  
             
        elif line.startswith('Grbl'):
            self.SocketEmit('console', {'data': line, 'class': 'recive'})
            
        elif line.startswith('error'):
            self.SocketEmit('console', {'data': line, 'class': 'reciveError'})
            print(f'GRBL reports an error: {line}')
            self.KILLOPERATION = True   
            
        if self.connection.in_waiting < 15:
            time.sleep(0.05)
            
def StatusReportProcess(self, response):
        response = response.replace('<', '').replace('>', '').split('|')
        for item in response:
            if 'Idle' in item or 'Run' in item or 'Hold' in item or 'Jog' in item or 'Alarm' in item or 'Door' in item or 'Check' in item or 'Home' in item or 'Sleep' in item:
                if ':' in item:
                    self.Machinestatus, self.subStatus = item.split(':')
                    
                else:
                    self.Machinestatus = item
                    self.subStatus = None
            elif 'A' in item:
                self.accessoryState = list(item)                    #OPTIMIZE with .startswith()
            elif 'FS' in item:
                FS = item.replace('FS:', '').split(',')
                self.RealFeed = float(FS[0])
                self.RealSpindle = float(FS[1])
            
            elif 'F' in item:
                self.RealFeed = float(item.replace('F:', ''))
                
            elif 'WPos' in item:
                value = item.replace('WPos:', '')
                self.Wpos = list(map(float, value.split(',')))
                self.Mpos = [self.Wpos[0] + self.WCO[0], self.Wpos[1] + self.WCO[1], self.Wpos[2] + self.WCO[2]]
                
            elif 'MPos' in item:
                value = item.replace('MPos:', '')
                self.Mpos = list(map(float, value.split(',')))
                self.Wpos = [self.Mpos[0] - self.WCO[0], self.Mpos[1] - self.WCO[1], self.Mpos[2] - self.WCO[2]]
                
            elif 'WCO' in item:
                value = item.replace('WCO:', '')
                self.WCO = list(map(float, value.split(',')))
                
            elif 'Ov' in item:
                value = item.replace('Ov:', '')
                self.Ov = list(map(float, value.split(',')))
                self.SocketEmit('Overides', self.Ov)
                
            elif 'Ln' in item:
                self.LineNum = int(item)
                
            elif 'Pn' in item:
                self.triggeredPins = list(item)
                
def processGRBLSetting(self, data):
    data = data.split('=')
    self.settings[data[0]] = data[1]