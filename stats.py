'''
Created on 17 de mai de 2017

@author: fvj
'''
import base64, zlib

STATS_FILE = '6players.txt'

HAND_DESCRIPTION = ['No pair', 'Pair', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', \
                    'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']

def sort_file():
    try:
        stats_file = open(STATS_FILE, 'r+')
    except:
        print('ERROR: While opening stats file!')
        return
    
    entries = []    
    for line in stats_file.readlines():
        entries.append(line)
        
#     entries.sort(reverse=True)
    entries.sort()
    
    stats_file.seek(0)
    stats_file.truncate()
      
    for entry in entries:
        stats_file.write(entry)
        
    stats_file.close()
    
    stats = [0 for _ in range(len(HAND_DESCRIPTION))]
    for i in range(len(entries)):
        hand = int(entries[i][2])
        stats[hand] += 1
    
    print('Sorted {} entries:'.format(len(entries)))
    for i in range(len(HAND_DESCRIPTION)):
        print('{:6.2f} % | {}'.format(100*stats[i]/len(entries), HAND_DESCRIPTION[i]))

def lookup(hand_code):
    try:
        stats_file = open(STATS_FILE, 'r')
    except:
        print('ERROR: While opening stats file!')
        return -1
    
    entries = []    
    for line in stats_file.readlines():
        entries.append(line)
        
    entries.sort()
    
    for i in range(len(entries)):
        if int(entries[i], 16) >= hand_code:
            return i/len(entries)
    return -1

def compress():
    try:
        stats_file = open(STATS_FILE, 'r+')
    except:
        print('ERROR: While opening stats file!')
        return
    
    content = stats_file.read()
    content = base64.b64encode(zlib.compress(str.encode(content), 9)).decode("utf-8")
    
    stats_file.seek(0)
    stats_file.truncate()
    stats_file.write(content)
    stats_file.close()
    print('Compression complete!')

def decompress():
    try:
        stats_file = open(STATS_FILE, 'r+')
    except:
        print('ERROR: While opening stats file!')
        return
    
    content = stats_file.read()
    content = zlib.decompress(base64.b64decode(content)).decode("utf-8")
    
    stats_file.seek(0)
    stats_file.truncate()
    stats_file.write(content)
    stats_file.close()
    print('Decompression complete!')

if __name__ == '__main__':
#     print('Your hand is better than {:.1f}% of winning hands!'.format(100*lookup(0x4c0000)))
#     compress()
#     decompress()
    sort_file()