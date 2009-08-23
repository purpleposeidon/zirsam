
f = open("items.csv")
selmaho_list = open("selma").read().split()
d = {}
for s in selmaho_list:
  d[s] = []

for line in f:
  c, s = line.split('\t')
  c = c.strip()
  if not '*' in s:
    for selmaho in selmaho_list:
      s = s.strip().replace('1', '').replace('2', '').replace('3', '').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','')
      if selmaho == s:
        d[selmaho].append(c)



for key in d:
  l = ''
  for i in d[key]:
    l += i + ' '
  l = l.strip().replace('.', '')
  print("%s = selmaho(%r, %r)" % (key, key, l))


