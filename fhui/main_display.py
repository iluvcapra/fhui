from typing import List
from dataclasses import dataclass 


# from fhui.message_update import MessageUpdate

# @dataclass
# class MainDisplay:
#     display_cells: List[int]

#     @dataclass
#     class Update(MessageUpdate):
#         zone: int
#         chardata: List[int]
        
#         @classmethod
#         def from_midi(cls, data) -> List['Update']:
#             i = iter(data)
#             retval = list()
#             while True:
#                 n = next(i, None)
#                 if n == 0xf7:
#                     break

#                 elif n & 0x0f < 0x08:
#                     zone = n
#                     data = [next(i), next(i), next(i), next(i), 
#                             next(i), next(i), next(i), next(i),
#                             next(i), next(i)]

                    #elem = cls(zone=zone, chardata=data)
                    #retval.append(elem)

                #elif n == None:
                    #raise Exception("Malformed Large Display sysex update")
                #else:
                    #raise Exception("Unexpected Large Display zone")

            #return retval 

    #def __init__(self):
        #self.display_zones = list()
        #for i in range(0,80):
            #display_cells[i] = 0x20

    #def line1(self) -> List[int]:
        #retval = " " * 40
        #for i in range(0,40):
            #retval[i] = display_cells.get(i, 0x20)

        #return retval

    #def line2(self) -> List[int]:
        #retval = " " * 40
        #for i in range(40,80):
            #retval[i] = display_cells.get(i, 0x20)

        #return retval
    
    #def update(self, updates: List[Update]):
        #for update in updates:
            #if update.zone not in range(0,8) or len(update.chardata) < 10:
                ##fixme this is an error
                #return
            
            #for i in range(0,10):
                #display_cells[update.zone*10 + i] = update.chardata[i]



