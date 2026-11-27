"""Derive road-centred navigation from the illustrated map and hand-picked guide points."""
from PIL import Image,ImageDraw
from scipy import ndimage
import numpy as np,json,heapq
from pathlib import Path
G=json.load(open('scripts/map-guides.json'))
source=Image.open('dist/assets/approved-worlds.png').convert('RGB')
# Fix guide routes that previously crossed the lobes or used the wrong incoming lane.
G['routes'][5]=[[[535,767],[555,757],[575,725],[610,701],[640,703],[672,721],[704,750],[730,776],[760,806],[790,829],[821,840],[849,833],[876,813],[891,787],[895,769],[885,740],[861,712],[834,701],[806,703],[775,721],[746,750],[719,779],[690,810],[660,833],[631,841],[603,836],[579,821],[562,797],[555,771],[567,737],[591,713],[620,701],[650,707],[680,728],[710,756],[735,770],[758,748],[784,722],[809,706],[836,701],[860,712],[883,739],[895,767],[928,771],[981,771]]]
G['routes'][8][0]=[[24,1344],[85,1344],[127,1340],[145,1323],[158,1301],[176,1287],[210,1286],[253,1286],[253,1344]]
G['routes'][8][2]=[[487,1343],[444,1343],[410,1340],[390,1324],[378,1310],[352,1307],[329,1315],[324,1343],[309,1356],[283,1354],[257,1344]]
# Homeworld has four drawn entrances. Follow each directly to the shared approach.
G['routes'][9]=[[[537,1318],[572,1315],[597,1302],[616,1276],[646,1272],[667,1259],[683,1230],[677,1265],[661,1296],[660,1320],[676,1343],[707,1361],[741,1371],[774,1373],[808,1364],[838,1346],[864,1332],[893,1329],[928,1340],[972,1351]],[[537,1419],[570,1417],[600,1405],[627,1385],[655,1375],[690,1374],[727,1376],[763,1377],[802,1370],[838,1346],[864,1332],[893,1329],[928,1340],[972,1351]],[[835,1230],[834,1251],[817,1271],[797,1296],[782,1324],[783,1342],[793,1358],[808,1364],[838,1346],[864,1332],[893,1329],[928,1340],[972,1351]],[[835,1499],[830,1476],[807,1459],[793,1440],[794,1421],[810,1401],[828,1383],[836,1363],[838,1346],[864,1332],[893,1329],[928,1340],[972,1351]]]
G['routes'][1]=[[[533,245],[572,235],[620,235],[657,222],[664,180],[665,157],[682,143],[731,143],[755,152],[779,174],[840,175],[887,175],[908,194],[898,216],[874,221],[760,221],[736,227],[724,245],[724,264],[699,282],[657,284],[629,301],[634,320],[655,332],[715,332],[758,330],[783,317],[793,292],[794,278],[818,265],[916,265],[945,251],[972,235]]]
G['routes'][3]=[[[536,511],[579,511],[602,501],[615,478],[632,458],[662,431],[712,413],[772,406],[835,415],[896,438],[936,471],[956,511],[949,548],[922,580],[879,603],[819,615],[759,618],[706,608],[672,588],[659,558],[662,521],[679,488],[706,461],[746,445],[792,445],[842,455],[869,478],[879,505],[869,535],[839,555],[799,560],[759,551],[741,535],[739,511],[752,493],[776,485],[790,508]]]
G['routes'][5]=[[[535,767],[566,771],[580,733],[607,708],[642,700],[675,708],[701,730],[725,755],[750,783],[777,815],[809,838],[850,849],[887,840],[916,819],[931,790],[941,773],[930,748],[918,718],[894,700],[860,697],[828,704],[799,725],[772,751],[745,779],[720,808],[691,834],[656,848],[620,844],[595,828],[579,805],[566,772],[580,733],[607,708],[642,700],[675,708],[701,730],[725,755],[741,771],[772,751],[799,725],[828,704],[860,697],[894,700],[918,718],[930,748],[941,773],[986,771]]]
result=[];debug=source.copy();draw=ImageDraw.Draw(debug)
for i,((ox,oy,w,h),routes) in enumerate(zip(G['panels'],G['routes'])):
 im=np.array(source.crop((ox,oy,ox+w,oy+h))).astype(float);r,g,b=im[:,:,0],im[:,:,1],im[:,:,2]
 if i in (0,2): mask=(r>140)&(g>120)&(b>80)&(r>g*1.06)&(g>b*1.05)
 elif i in (1,7):mask=(r>175)&(g>145)&(b>100)&(r>g*1.03)&(g>b*1.08)
 elif i==3: mask=(r>150)&(g>110)&(b>100)&(r>g*1.08)&(r>b*1.02)&(b<g*1.24)
 elif i in (4,5):mask=(r>145)&(g>115)&(b>80)&(r>g*1.07)&(g>b*1.02)
 elif i==6:mask=(r>140)&(g>120)&(b>85)&(r>g*1.045)&(g>b*1.03)
 else:mask=(r>145)&(g>115)&(b>90)&(r>g*1.07)&(r>b*1.08)&(g>b*.96)
 mask=ndimage.binary_closing(mask,iterations=2)
 inside=ndimage.distance_transform_edt(mask);outside=ndimage.distance_transform_edt(~mask)
 # Discourage off-road traversal and reward a route down the broad middle of the road.
 cost=1+16/(inside+1)+outside*35
 def snap(pt):
  x,y=pt[0]-ox,pt[1]-oy;xx,yy=np.meshgrid(np.arange(max(0,int(x)-17),min(w,int(x)+18)),np.arange(max(0,int(y)-17),min(h,int(y)+18)))
  score=inside[yy,xx]*2.5-np.hypot(xx-x,yy-y);j=np.argmax(score);return int(xx.flat[j]),int(yy.flat[j])
 def connect(a,z):
  todo=[(0,a)];dist={a:0};prev={};bounds=(max(0,min(a[0],z[0])-30),min(w-1,max(a[0],z[0])+30),max(0,min(a[1],z[1])-30),min(h-1,max(a[1],z[1])+30))
  while todo:
   d,p=heapq.heappop(todo)
   if d!=dist.get(p):continue
   if p==z:break
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
    q=p[0]+dx,p[1]+dy
    if not(bounds[0]<=q[0]<=bounds[1] and bounds[2]<=q[1]<=bounds[3]):continue
    nd=d+(cost[q[1],q[0]]+cost[p[1],p[0]])*.5*(1.414 if dx and dy else 1)
    if nd<dist.get(q,float('inf')):dist[q]=nd;prev[q]=p;heapq.heappush(todo,(nd,q))
  if z not in dist:raise Exception('No route')
  path=[z]
  while path[-1]!=a:path.append(prev[path[-1]])
  return path[::-1]
 out=[]
 for route in routes:
  if i==5:
   out.append([{'x':round((x-ox)*1000/w,2),'y':round((y-oy)*600/h,2)} for x,y in route]);draw.line([tuple(p) for p in route],fill='#ff2222',width=2);continue
  anchors=[snap(p) for p in route];path=[]
  for a,z in zip(anchors,anchors[1:]):path+=connect(a,z)[:-1]
  path.append(anchors[-1])
  # Remove short out-and-back detours caused by guide points adjacent to props.
  clean=[];seen={}
  for q in path:
   if q in seen and len(clean)-seen[q]<70:
    index=seen[q]
    for dead in clean[index+1:]:seen.pop(dead,None)
    clean=clean[:index+1]
   else:seen[q]=len(clean);clean.append(q)
  path=clean[::3]+[clean[-1]]
  # Keep unit feet anchored to the navigation point, not the centre of their sprite.
  world=[{'x':round(x*1000/w,2),'y':round(y*600/h,2)} for x,y in path];out.append(world)
  draw.line([(x+ox,y+oy) for x,y in path],fill='#ff2222',width=2)
 result.append(out)
Path('dist/assets/navigation.json').write_text(json.dumps(result,separators=(',',':')))
debug.save('/tmp/refined-paths.png')
print('Road-centred routes generated for all ten planets')

# Preserve the portal centreline instead of snapping its first steps onto nearby grass.
p=Path('dist/assets/navigation.json')
routes=json.loads(p.read_text())
r=routes[0][0]
join=next(i for i,q in enumerate(r) if q['x']>=122)
routes[0][0]=[{'x':26.05,'y':268.97},{'x':74.15,'y':268.97}]+r[join:]
p.write_text(json.dumps(routes,separators=(',',':')))

# Cross the gates on the road centre rather than routing around their visible stonework.
p=Path('dist/assets/navigation.json')
routes=json.loads(p.read_text())
fixes=[(360,660,[(360,95),(400,102),(440,111),(480,122),(520,133),(560,141),(600,146),(640,160),(660,180)]),(360,610,[(360,450),(400,451),(440,452),(480,452),(520,452),(560,452),(600,450),(610,446)])]
for j,(lo,hi,points) in enumerate(fixes):
 r=routes[7][j]
 routes[7][j]=[p for p in r if p['x']<lo]+[dict(x=x,y=y) for x,y in points]+[p for p in r if p['x']>hi]
p.write_text(json.dumps(routes,separators=(',',':')))
