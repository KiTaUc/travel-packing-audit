import argparse,json
from collections import defaultdict
from datetime import date
from pathlib import Path
def run(data, today='', days=0):
 if 'packing'=='segments': return {'segments':len(data),'total_seconds':sum(int(x['seconds']) for x in data),'timeline':[{'title':x['title'],'start_seconds':sum(int(y['seconds']) for y in data[:i])} for i,x in enumerate(data)]}
 if 'packing'=='shots': return {k:[x['shot'] for x in data if x['stage']==k and not x['done']] for k in sorted({x['stage'] for x in data})}
 if 'packing'=='print': return {**data,'total':round(int(data['quantity'])*float(data['unit_price']),2),'ready':data['status']=='ready'}
 if 'packing'=='time':
  out=defaultdict(int)
  for x in data: out[x['client']]+=int(x['minutes'])
  return dict(out)
 if 'packing'=='deadline': return sorted([x for x in data if not x['done'] and 0 <= (date.fromisoformat(x['due_on'])-date.fromisoformat(today)).days <= days],key=lambda x:x['due_on'])
 if 'packing'=='slots': return [{**x,'free':int(x['capacity'])-len(x['people'])} for x in data]
 if 'packing'=='harvest':
  out=defaultdict(float)
  for x in data: out[x['field']+' · '+x['crop']]+=float(x['kg'])
  return dict(out)
 if 'packing'=='water': return [{'zone':x['zone'],'liters':round(int(x['minutes'])*float(x['liters_per_minute']),2)} for x in data]
 if 'packing'=='packing':
  out=defaultdict(list)
  for x in data:
   if not x['packed']: out[x['category']].append(x['item'])
  return dict(out)
 return {'visit_date':data['visit_date'],'done':data.get('done',[]),'next':data.get('next',[])}
def main():
 p=argparse.ArgumentParser();p.add_argument('command');p.add_argument('file',type=Path);p.add_argument('--today',default='');p.add_argument('--days',type=int,default=0);x=p.parse_args();print(json.dumps(run(json.loads(x.file.read_text(encoding='utf-8')),x.today,x.days),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
