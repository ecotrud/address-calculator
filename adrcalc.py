# given an IPv4 address and a subnet mask, compute the network,
# broadcast, and first/last host addresses


# convert the parameter decimal integer to a binary (string) with more usable format for network addresses
def dec_to_bin(num):
    temp = bin(int(num[0:3]))[2:]
    if(temp=="0"):
        result = "00000000"
    else:
        result = temp
    for x in range(1,4):
        temp = bin(int(num[x*4:x*4+3]))[2:]
        if(temp=="0"):
            result = result + "." + "00000000"
        else:
            result = result + "." + temp
    return result

def find_adr(i,s):
    # determine network address through examining position of zeros in the subnet mask
    findzero = s.find("0")
    if(findzero==-1):
        n = i
        return n + "/32", n, n, n
    else:
        # magic is needed to calculate the slash notation
        if(findzero>-1 and findzero<8):
            magic = 32
        elif(findzero>8 and findzero<17):
            magic = 33
        elif(findzero>17 and findzero<26):
            magic = 34
        elif(findzero>26 and findzero<35):
            magic = 35
        n = i[:findzero] + "0" * (35 - findzero)
        # replacing specific characters (i.e. not removing needed information) with dots for formatting
        n_new = n[:8] + "." + n[9:17] + "." + n[18:26] + "." + n[27:]
        # use original n to calculate broadcast address, then format it the same way we did n_new
        b = n[:findzero] + "1" * (35 - findzero)
        b_new = b[:8] + "." + b[9:17] + "." + b[18:26] + "." + b[27:]
        # calculate the first and last hosts by converting parts of the network and broadcast addresses
        # between dec<->bin, and then check to make sure they are correct
        f = n_new[:27] + ("0" * len(bin(int(n_new[27:],2) + 1)[2:])) + bin(int(n_new[27:],2) + 1)[2:]
        l = b_new[:27] + ("0" * len(bin(int(b_new[27:],2) - 1)[2:])) + bin(int(b_new[27:],2) - 1)[2:]
        if(int(l[27:],2)<int(f[27:],2)):
            temp = f
            f = l
            l = temp
        return n_new + "/" + magic, b_new, f, l


# take input for IPv4 address and subnet mask
ip_address_dec = input("enter the ipv4 address in decimal, placing a 0 in empty digits (i.e. '064' instead of '64'): ")
submask_dec = input("enter the subnet mask in decimal, placing a 0 in empty digits (i.e. '064' instead of '64'): ")
# convert user-given values to binary
ip_address_bin = dec_to_bin(ip_address_dec)
submask_bin = dec_to_bin(submask_dec)
# pass the converted values to a function to determine the network, broadcast, and first/last host addresses
network_address_bin, broadcast_address_bin, first_host_bin, last_host_bin = find_adr(ip_address_bin, submask_bin)