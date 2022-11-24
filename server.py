import socket
def xor(a, b):
  result = []
  for i in range(1, len(b)):
    if a[i] == b[i]:
      result.append("0")
    else:
      result.append("1")
  return "".join(result)


def mod2div(divident, divisor):
  pick = len(divisor)
  tmp = divident[0:pick]
  while pick < len(divident):
    if tmp[0] == "1":
      tmp = xor(divisor, tmp) + divident[pick]
    else:
      tmp = xor("0" * pick, tmp) + divident[pick]
    pick += 1
  if tmp[0] == "1":
    tmp = xor(divisor, tmp)
  else:
    tmp = xor("0" * pick, tmp)
  checkword = tmp
  return checkword


def decodes(data, key,p):
  l_key = len(key)
  if p==True:
    appended_data = data.decode() + "0" * (l_key - 1)
  else:
    appended_data = data + "0" * (l_key - 1)
  remainder = mod2div(appended_data, key)
  return remainder


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8006))
s.listen(1)
print("Socket is listening for Client")

while True:
  c, addr = s.accept()
  print("Connection Established", addr)
  data = c.recv(1024)
  print("Received encoded data:", data.decode())
  if not data:
    break
  dat = data.decode()
  key = input("Enter divisor :")
  ans = decodes(data, key,True)
  print("Remainder is :" + ans)
  dat = list(dat)
  val = input("Do you want to introduce error (1 for yes:0 for no): ")

  if val == "1":
    err = int(input("Enter the Error position : "))
    if dat[len(dat) - err] == "1":
      dat[len(dat) - err] = "0"
    else:
      dat[len(dat) - err] = "1"
  dat1 = "".join(dat)
  temp = "0" * (len(key) - 1)
  if dat1 == data.decode():
    c.sendall((dat1 + "\nNo error").encode())
  else:
    key = input("Enter divisor :")
    ans = decodes(dat1, key,False)
    print("Remainder is :" + ans)
    c.sendall(("Errored data is:" + dat1).encode())
    break
  c.close()
