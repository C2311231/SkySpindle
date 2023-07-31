import grblCom


GRBL = grblCom.GRBLConection('COM5', 115200)
print(GRBL.GetGRBLSettings())