Flow of the code
Client Side: main client_side.py
1.	Packets:
  a.	Def encryption type -> choose either encrypted or unencrypted by entering 0(unencrypted) or 1 (encrypted)  
  b.	Def start_packet-> Creating start packet (SS) with packet type (SS), RFMP (protocol name), v1.0 (Version 1), and encrypted flag (0 or 1)
  c.	Def packet_formatter -> adds parentheses and commas
2.	Client_side:
  a.	Def main -> sends SS packet to server side with s.send
Server Side: main is in server side
3.	Main in server side
  a.	Def chatting -> starts by receiving and unencrypting from utf-8 (with sockets have to be sent in bytes)
4.	Checks
  a.	Def is_secure -> checks if SS packet ends in 0 or 1 so unencrypted or encrypted. Returns true if encrypted and false if unencrypted
5.	Main in server side
  a.	If step 4 is true so encrypted then sending connection packet (CC packet) by calling step 6
6.	Packets (builds CC packet depending on if encryption or not)
  a.	If not encrypted then just CC and if encrypted then CC + RSA public of server (originally in bytes -> then converted to string so user can see -> encrypted again to send)
7.	Main in server side
  a.	Sending cc + rsa public key packet in if_secure by sending_secure_connection_packet 
  b.	 just cc if in na_secure_packet so unsecure communication
Client Side:
8.	Main in client side
  a.	Check when CC packet arrives the length of server response 	
    i.	2 -> unencrypted
    ii.	>2 -> encrypted
9.	IF ENCRYTPED-> Helpers
  a.	Then RSA public key converted from bytes to string 
  b.	Passed to algo_and_encrypted_session
10.	Packets
  a.	Build EC packet
    i.	 Def encryption choice -> client chooses aes or Caesar
    ii.	Def algo_and_encrypted_session 
      1.	If aes:
          a.	generates session key
          b.	encrypt session key with rsa public key
          c.	convert that to bytes
      2.	If Caesar:
          a.	Generates integer to shift
          b.	Encrypt that with rsa public key
          c.	Convert that to bytes
    iii.	Def ec_packet
      1.	Brings all information together and returns completed ec packet with (EC, Algo -> Caesar or Aes, Encrypted Session key (by server rsa public key, Client public key)
11.	Client_side main function
  a.	Sending EC-packet to server

Sever side:
12.	Server side main function
  a.	Waiting for EC packet  to arrive 
13.	Decryption
  a.	Decrypt_ec_packet
      i.	Split ec packet to get algorithm, encrypted session key & client public key
      ii.	Decrypt session key with help of server private key 