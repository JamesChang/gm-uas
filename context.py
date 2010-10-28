delay_service = None

#game result for dota
def make_game_result():
  from protobuf.res_gameres_pb2 import GameMessage
  rst = GameMessage()
  war3 = rst.war3.add()
  war3.header.war3Version="War3-1.23-6352"
  war3.header.messageType = "game result"
  war3.header.battleType="Dota"
  war3.header.time = 33225
  war3.header.userIDOfSender = 12345
  d = rst.SerializeToString()
  import base64
  d=base64.standard_b64encode(d)
  return d
game_result = make_game_result()

