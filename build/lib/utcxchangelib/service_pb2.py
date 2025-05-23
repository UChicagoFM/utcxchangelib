# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\x07manager\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xe1\x01\n\x17\x43lientMessageToExchange\x12\x34\n\x0c\x61uthenticate\x18\x01 \x01(\x0b\x32\x1c.manager.AuthenticateRequestH\x00\x12-\n\tnew_order\x18\x02 \x01(\x0b\x32\x18.manager.NewOrderRequestH\x00\x12\x33\n\x0c\x63\x61ncel_order\x18\x03 \x01(\x0b\x32\x1b.manager.CancelOrderRequestH\x00\x12$\n\x04swap\x18\x04 \x01(\x0b\x32\x14.manager.SwapRequestH\x00\x42\x06\n\x04\x62ody\"\xc9\x04\n\x17\x45xchangeMessageToClient\x12\r\n\x05index\x18\x02 \x02(\x04\x12\x36\n\rauthenticated\x18\x01 \x01(\x0b\x32\x1d.manager.AuthenticateResponseH\x00\x12&\n\x05trade\x18\x04 \x01(\x0b\x32\x15.manager.TradeMessageH\x00\x12/\n\norder_fill\x18\x05 \x01(\x0b\x32\x19.manager.OrderFillMessageH\x00\x12\x37\n\x0eorder_rejected\x18\x06 \x01(\x0b\x32\x1d.manager.OrderRejectedMessageH\x00\x12\x37\n\x0f\x63\x61ncel_response\x18\x07 \x01(\x0b\x32\x1c.manager.CancelOrderResponseH\x00\x12.\n\rswap_response\x18\x08 \x01(\x0b\x32\x15.manager.SwapResponseH\x00\x12.\n\rbook_snapshot\x18\x0b \x01(\x0b\x32\x15.manager.BookSnapshotH\x00\x12*\n\x0b\x62ook_update\x18\r \x01(\x0b\x32\x13.manager.BookUpdateH\x00\x12\x36\n\x11position_snapshot\x18\x0c \x01(\x0b\x32\x19.manager.PositionResponseH\x00\x12(\n\nnews_event\x18\x0e \x01(\x0b\x32\x12.manager.NewsEventH\x00\x12&\n\x05\x65rror\x18\t \x01(\x0b\x32\x15.manager.ErrorMessageH\x00\x42\x06\n\x04\x62ody\"\x97\x02\n\x16KafkaMessageToExchange\x12\x0c\n\x04user\x18\x01 \x02(\t\x12-\n\tnew_order\x18\x04 \x01(\x0b\x32\x18.manager.NewOrderRequestH\x00\x12\x33\n\x0c\x63\x61ncel_order\x18\x05 \x01(\x0b\x32\x1b.manager.CancelOrderRequestH\x00\x12$\n\x04swap\x18\x06 \x01(\x0b\x32\x14.manager.SwapRequestH\x00\x12\x33\n\x0fsnapshotRequest\x18\x07 \x01(\x0b\x32\x18.manager.SnapshotRequestH\x00\x12(\n\nnews_event\x18\x08 \x01(\x0b\x32\x12.manager.NewsEventH\x00\x42\x06\n\x04\x64\x61ta\"\x84\x05\n\x18KafkaMessageFromExchange\x12\x1b\n\x04\x61ttn\x18\x01 \x02(\x0b\x32\r.manager.Attn\x12\r\n\x05index\x18\x03 \x02(\x04\x12&\n\x05trade\x18\x06 \x01(\x0b\x32\x15.manager.TradeMessageH\x00\x12/\n\norder_fill\x18\x07 \x01(\x0b\x32\x19.manager.OrderFillMessageH\x00\x12\x37\n\x0f\x63\x61ncel_response\x18\x08 \x01(\x0b\x32\x1c.manager.CancelOrderResponseH\x00\x12\x35\n\x0corder_reject\x18\t \x01(\x0b\x32\x1d.manager.OrderRejectedMessageH\x00\x12%\n\x04swap\x18\n \x01(\x0b\x32\x15.manager.SwapResponseH\x00\x12.\n\rbook_snapshot\x18\x0b \x01(\x0b\x32\x15.manager.BookSnapshotH\x00\x12*\n\x0b\x62ook_update\x18\r \x01(\x0b\x32\x13.manager.BookUpdateH\x00\x12*\n\x0b\x63\x61sh_update\x18\x0e \x01(\x0b\x32\x13.manager.CashUpdateH\x00\x12\x32\n\x0fposition_update\x18\x0f \x01(\x0b\x32\x17.manager.PositionUpdateH\x00\x12\x36\n\x11position_snapshot\x18\x0c \x01(\x0b\x32\x19.manager.PositionResponseH\x00\x12(\n\nnews_event\x18\x10 \x01(\x0b\x32\x12.manager.NewsEventH\x00\x12&\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x15.manager.ErrorMessageH\x00\x42\x06\n\x04\x64\x61ta\")\n\nCashUpdate\x12\x0c\n\x04user\x18\x01 \x02(\t\x12\r\n\x05value\x18\x03 \x02(\x03\"=\n\x0ePositionUpdate\x12\x0c\n\x04user\x18\x01 \x02(\t\x12\x0e\n\x06symbol\x18\x02 \x02(\t\x12\r\n\x05value\x18\x03 \x02(\x03\"w\n\nBookUpdate\x12\x0e\n\x06symbol\x18\x01 \x02(\t\x12&\n\x04side\x18\x02 \x02(\x0e\x32\x18.manager.BookUpdate.Side\x12\n\n\x02px\x18\x03 \x02(\x04\x12\n\n\x02\x64q\x18\x04 \x02(\x03\"\x19\n\x04Side\x12\x07\n\x03\x42UY\x10\x01\x12\x08\n\x04SELL\x10\x02\"\x1f\n\x0fSnapshotRequest\x12\x0c\n\x04user\x18\x01 \x02(\t\"F\n\x10PositionResponse\x12\x0c\n\x04\x63\x61sh\x18\x01 \x02(\x03\x12$\n\tpositions\x18\x02 \x03(\x0b\x32\x11.manager.Position\",\n\x08Position\x12\x0e\n\x06symbol\x18\x01 \x02(\t\x12\x10\n\x08position\x18\x02 \x02(\x03\"b\n\x0c\x42ookSnapshot\x12\x0e\n\x06symbol\x18\x01 \x02(\t\x12 \n\x04\x62ids\x18\x02 \x03(\x0b\x32\x12.manager.BookOrder\x12 \n\x04\x61sks\x18\x03 \x03(\x0b\x32\x12.manager.BookOrder\"$\n\tBookOrder\x12\n\n\x02px\x18\x01 \x02(\x04\x12\x0b\n\x03qty\x18\x02 \x02(\x04\"*\n\tBookError\x12\x0e\n\x06symbol\x18\x01 \x02(\t\x12\r\n\x05\x65rror\x18\x02 \x02(\t\"\x98\x01\n\tNewsEvent\x12-\n\nstructured\x18\x0e \x01(\x0b\x32\x17.manager.StructuredNewsH\x00\x12\x31\n\x0cunstructured\x18\x0f \x01(\x0b\x32\x19.manager.UnstructuredNewsH\x00\x12\x11\n\ttimestamp\x18\x01 \x02(\x04\x12\x0e\n\x06symbol\x18\x02 \x02(\tB\x06\n\x04\x64\x61ta\"i\n\x0eStructuredNews\x12%\n\x08\x65\x61rnings\x18\x01 \x01(\x0b\x32\x11.manager.EarningsH\x00\x12%\n\x08petition\x18\x02 \x01(\x0b\x32\x11.manager.PetitionH\x00\x42\t\n\x07subtype\"(\n\x08\x45\x61rnings\x12\r\n\x05\x61sset\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\x01\"E\n\x08Petition\x12\r\n\x05\x61sset\x18\x01 \x02(\t\x12\x16\n\x0enew_signatures\x18\x02 \x02(\r\x12\x12\n\ncumulative\x18\x03 \x02(\r\"9\n\x10UnstructuredNews\x12\x14\n\x0cmessage_type\x18\x01 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x02(\t\"b\n\x13\x43\x61ncelOrderResponse\x12\n\n\x02id\x18\x01 \x02(\t\x12$\n\x02ok\x18\x02 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12\x0f\n\x05\x65rror\x18\x03 \x01(\tH\x00\x42\x08\n\x06result\"5\n\x13\x43loseTradingRequest\x12\x0e\n\x06worker\x18\x01 \x02(\t\x12\x0e\n\x06symbol\x18\x02 \x02(\t\"4\n\x12OpenTradingRequest\x12\x0e\n\x06worker\x18\x01 \x02(\t\x12\x0e\n\x06symbol\x18\x02 \x02(\t\"!\n\x11KillWorkerRequest\x12\x0c\n\x04name\x18\x01 \x02(\t\"(\n\x0bSwapRequest\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0b\n\x03qty\x18\x02 \x02(\x04\"v\n\x0cSwapResponse\x12%\n\x07request\x18\x01 \x02(\x0b\x32\x14.manager.SwapRequest\x12$\n\x02ok\x18\x02 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12\x0f\n\x05\x65rror\x18\x03 \x01(\tH\x00\x42\x08\n\x06result\"\x14\n\x12KillWorkerResponse\"\x1e\n\x0c\x45rrorMessage\x12\x0e\n\x06reason\x18\x01 \x02(\t\"7\n\x0cTradeMessage\x12\x0e\n\x06symbol\x18\x01 \x02(\t\x12\n\n\x02px\x18\x02 \x02(\x04\x12\x0b\n\x03qty\x18\x03 \x02(\x04\"7\n\x10OrderFillMessage\x12\n\n\x02id\x18\x01 \x02(\t\x12\x0b\n\x03qty\x18\x02 \x02(\x04\x12\n\n\x02px\x18\x03 \x02(\x04\"2\n\x14OrderRejectedMessage\x12\n\n\x02id\x18\x01 \x02(\t\x12\x0e\n\x06reason\x18\x02 \x02(\t\"\xcb\x01\n\x0fNewOrderRequest\x12\x0e\n\x06symbol\x18\x02 \x02(\t\x12\n\n\x02id\x18\x03 \x02(\t\x12+\n\x04side\x18\x06 \x02(\x0e\x32\x1d.manager.NewOrderRequest.Side\x12$\n\x05limit\x18\x07 \x01(\x0b\x32\x13.manager.LimitOrderH\x00\x12&\n\x06market\x18\x08 \x01(\x0b\x32\x14.manager.MarketOrderH\x00\"\x19\n\x04Side\x12\x07\n\x03\x42UY\x10\x01\x12\x08\n\x04SELL\x10\x02\x42\x06\n\x04kind\"%\n\nLimitOrder\x12\x0b\n\x03qty\x18\x04 \x02(\x04\x12\n\n\x02px\x18\x05 \x02(\x04\"\x1a\n\x0bMarketOrder\x12\x0b\n\x03qty\x18\x04 \x02(\x04\" \n\x12\x43\x61ncelOrderRequest\x12\n\n\x02id\x18\x01 \x02(\t\"9\n\x13\x41uthenticateRequest\x12\x10\n\x08username\x18\x01 \x02(\t\x12\x10\n\x08password\x18\x02 \x02(\t\"\'\n\x14\x41uthenticateResponse\x12\x0f\n\x07success\x18\x01 \x02(\x08\"\x1a\n\x0bWorkerError\x12\x0b\n\x03why\x18\x01 \x02(\t\"\x1c\n\rExchangeError\x12\x0b\n\x03why\x18\x01 \x02(\t\"\x1e\n\x0bOpenTrading\x12\x0f\n\x07symbols\x18\x02 \x03(\t\"\x1f\n\x0c\x43loseTrading\x12\x0f\n\x07symbols\x18\x03 \x03(\t\"\"\n\x12StartWorkerRequest\x12\x0c\n\x04name\x18\x01 \x02(\t\"\'\n\x04\x41ttn\x12\x10\n\x08\x65veryone\x18\x02 \x02(\x08\x12\r\n\x05users\x18\x03 \x03(\t\"\x15\n\x13StartWorkerResponse\"\x14\n\x12ListWorkersRequest\"_\n\nWorkerInfo\x12\x0c\n\x04name\x18\x01 \x02(\t\x12.\n\nstart_time\x18\x02 \x02(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0b\x65xit_status\x18\x03 \x01(\x05\"8\n\x13ListWorkersResponse\x12!\n\x04info\x18\x01 \x03(\x0b\x32\x13.manager.WorkerInfo2\xe8\x01\n\x05\x41\x64min\x12J\n\x0bStartWorker\x12\x1b.manager.StartWorkerRequest\x1a\x1c.manager.StartWorkerResponse\"\x00\x12G\n\nKillWorker\x12\x1a.manager.KillWorkerRequest\x1a\x1b.manager.KillWorkerResponse\"\x00\x12J\n\x0bListWorkers\x12\x1b.manager.ListWorkersRequest\x1a\x1c.manager.ListWorkersResponse\"\x00\x32[\n\x06\x43lient\x12Q\n\x05Start\x12 .manager.ClientMessageToExchange\x1a .manager.ExchangeMessageToClient\"\x00(\x01\x30\x01\x32\x0e\n\x0c\x45xchangeUser')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CLIENTMESSAGETOEXCHANGE']._serialized_start=89
  _globals['_CLIENTMESSAGETOEXCHANGE']._serialized_end=314
  _globals['_EXCHANGEMESSAGETOCLIENT']._serialized_start=317
  _globals['_EXCHANGEMESSAGETOCLIENT']._serialized_end=902
  _globals['_KAFKAMESSAGETOEXCHANGE']._serialized_start=905
  _globals['_KAFKAMESSAGETOEXCHANGE']._serialized_end=1184
  _globals['_KAFKAMESSAGEFROMEXCHANGE']._serialized_start=1187
  _globals['_KAFKAMESSAGEFROMEXCHANGE']._serialized_end=1831
  _globals['_CASHUPDATE']._serialized_start=1833
  _globals['_CASHUPDATE']._serialized_end=1874
  _globals['_POSITIONUPDATE']._serialized_start=1876
  _globals['_POSITIONUPDATE']._serialized_end=1937
  _globals['_BOOKUPDATE']._serialized_start=1939
  _globals['_BOOKUPDATE']._serialized_end=2058
  _globals['_BOOKUPDATE_SIDE']._serialized_start=2033
  _globals['_BOOKUPDATE_SIDE']._serialized_end=2058
  _globals['_SNAPSHOTREQUEST']._serialized_start=2060
  _globals['_SNAPSHOTREQUEST']._serialized_end=2091
  _globals['_POSITIONRESPONSE']._serialized_start=2093
  _globals['_POSITIONRESPONSE']._serialized_end=2163
  _globals['_POSITION']._serialized_start=2165
  _globals['_POSITION']._serialized_end=2209
  _globals['_BOOKSNAPSHOT']._serialized_start=2211
  _globals['_BOOKSNAPSHOT']._serialized_end=2309
  _globals['_BOOKORDER']._serialized_start=2311
  _globals['_BOOKORDER']._serialized_end=2347
  _globals['_BOOKERROR']._serialized_start=2349
  _globals['_BOOKERROR']._serialized_end=2391
  _globals['_NEWSEVENT']._serialized_start=2394
  _globals['_NEWSEVENT']._serialized_end=2546
  _globals['_STRUCTUREDNEWS']._serialized_start=2548
  _globals['_STRUCTUREDNEWS']._serialized_end=2653
  _globals['_EARNINGS']._serialized_start=2655
  _globals['_EARNINGS']._serialized_end=2695
  _globals['_PETITION']._serialized_start=2697
  _globals['_PETITION']._serialized_end=2766
  _globals['_UNSTRUCTUREDNEWS']._serialized_start=2768
  _globals['_UNSTRUCTUREDNEWS']._serialized_end=2825
  _globals['_CANCELORDERRESPONSE']._serialized_start=2827
  _globals['_CANCELORDERRESPONSE']._serialized_end=2925
  _globals['_CLOSETRADINGREQUEST']._serialized_start=2927
  _globals['_CLOSETRADINGREQUEST']._serialized_end=2980
  _globals['_OPENTRADINGREQUEST']._serialized_start=2982
  _globals['_OPENTRADINGREQUEST']._serialized_end=3034
  _globals['_KILLWORKERREQUEST']._serialized_start=3036
  _globals['_KILLWORKERREQUEST']._serialized_end=3069
  _globals['_SWAPREQUEST']._serialized_start=3071
  _globals['_SWAPREQUEST']._serialized_end=3111
  _globals['_SWAPRESPONSE']._serialized_start=3113
  _globals['_SWAPRESPONSE']._serialized_end=3231
  _globals['_KILLWORKERRESPONSE']._serialized_start=3233
  _globals['_KILLWORKERRESPONSE']._serialized_end=3253
  _globals['_ERRORMESSAGE']._serialized_start=3255
  _globals['_ERRORMESSAGE']._serialized_end=3285
  _globals['_TRADEMESSAGE']._serialized_start=3287
  _globals['_TRADEMESSAGE']._serialized_end=3342
  _globals['_ORDERFILLMESSAGE']._serialized_start=3344
  _globals['_ORDERFILLMESSAGE']._serialized_end=3399
  _globals['_ORDERREJECTEDMESSAGE']._serialized_start=3401
  _globals['_ORDERREJECTEDMESSAGE']._serialized_end=3451
  _globals['_NEWORDERREQUEST']._serialized_start=3454
  _globals['_NEWORDERREQUEST']._serialized_end=3657
  _globals['_NEWORDERREQUEST_SIDE']._serialized_start=2033
  _globals['_NEWORDERREQUEST_SIDE']._serialized_end=2058
  _globals['_LIMITORDER']._serialized_start=3659
  _globals['_LIMITORDER']._serialized_end=3696
  _globals['_MARKETORDER']._serialized_start=3698
  _globals['_MARKETORDER']._serialized_end=3724
  _globals['_CANCELORDERREQUEST']._serialized_start=3726
  _globals['_CANCELORDERREQUEST']._serialized_end=3758
  _globals['_AUTHENTICATEREQUEST']._serialized_start=3760
  _globals['_AUTHENTICATEREQUEST']._serialized_end=3817
  _globals['_AUTHENTICATERESPONSE']._serialized_start=3819
  _globals['_AUTHENTICATERESPONSE']._serialized_end=3858
  _globals['_WORKERERROR']._serialized_start=3860
  _globals['_WORKERERROR']._serialized_end=3886
  _globals['_EXCHANGEERROR']._serialized_start=3888
  _globals['_EXCHANGEERROR']._serialized_end=3916
  _globals['_OPENTRADING']._serialized_start=3918
  _globals['_OPENTRADING']._serialized_end=3948
  _globals['_CLOSETRADING']._serialized_start=3950
  _globals['_CLOSETRADING']._serialized_end=3981
  _globals['_STARTWORKERREQUEST']._serialized_start=3983
  _globals['_STARTWORKERREQUEST']._serialized_end=4017
  _globals['_ATTN']._serialized_start=4019
  _globals['_ATTN']._serialized_end=4058
  _globals['_STARTWORKERRESPONSE']._serialized_start=4060
  _globals['_STARTWORKERRESPONSE']._serialized_end=4081
  _globals['_LISTWORKERSREQUEST']._serialized_start=4083
  _globals['_LISTWORKERSREQUEST']._serialized_end=4103
  _globals['_WORKERINFO']._serialized_start=4105
  _globals['_WORKERINFO']._serialized_end=4200
  _globals['_LISTWORKERSRESPONSE']._serialized_start=4202
  _globals['_LISTWORKERSRESPONSE']._serialized_end=4258
  _globals['_ADMIN']._serialized_start=4261
  _globals['_ADMIN']._serialized_end=4493
  _globals['_CLIENT']._serialized_start=4495
  _globals['_CLIENT']._serialized_end=4586
  _globals['_EXCHANGEUSER']._serialized_start=4588
  _globals['_EXCHANGEUSER']._serialized_end=4602
# @@protoc_insertion_point(module_scope)
