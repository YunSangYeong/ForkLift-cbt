"""Deterministic authored study bank. No scraped past papers. Decimal half-up.
Concepts: 100. Numerical families: 30 × 30 conditions. Not an exam frequency model.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json, csv
ROOT=Path(__file__).resolve().parents[1]
SUBJECTS=['지게차 주행','화물 적재','운반','하역','안전관리']
SOURCE='https://github.com/YunSangYeong/ForkLift-cbt/blob/main/docs/question-review.md'
bank=[]
def make(subject,topic,stem,correct,wrong,explanation,idx,family=None,calc=None):
    choices=[correct]+wrong
    rotation=idx%4
    choices=choices[rotation:]+choices[:rotation]
    assert len(set(choices))==4
    q=dict(id=f'FL-{idx:04}',subject=subject,topic=topic,question=stem,choices=choices,answer=choices.index(correct)+1,explanation=explanation,difficulty='중',year=None,session=None,type='original',sourceUrl=SOURCE,verificationStatus='reviewed',reviewNote='AI 일반 지식과 명시된 기초 원리에 의한 자체 제작. 조건·보기·해설 내부 문장 검토. 외부 전문가 검수·공식 세부 기준 대조 미완료. 출처 링크는 작성·검토 내역이며 외부 정답 증빙이 아님.',version='main',rights='자체 제작 · CC BY 4.0 · ForkLift-cbt contributors')
    if family:q['family']=family;q['calculation']=calc;q['reviewNote']+=' 자체 제작 계산 변형: 독립 TypeScript 재계산 대상. 실제 장비 운용값·정격 판정에 사용하지 않음.'
    bank.append(q)
with (ROOT/'scripts/concepts.tsv').open() as f:
 for row in csv.reader(f,delimiter='\t'):
    assert len(row)==8,row
    subject,topic,stem,correct,*other=row
    make(subject,topic,stem,correct,other[:3],other[3],len(bank)+1)

def D(v):return Decimal(str(v))
def family(area,kind,topic,unit,build):
 for n in range(1,31):
    values,stem,result,explanation=build(n)
    result=D(result).quantize(D('.01'),rounding=ROUND_HALF_UP)
    def fmt(x):return format(x,'f').rstrip('0').rstrip('.') if '.' in format(x,'f') else str(x)
    delta=max(D('.01'),(abs(result)*D('.1')).quantize(D('.01'),rounding=ROUND_HALF_UP))
    wrong=[result+delta*i for i in ([-2,-1,1],[-1,1,2],[-2,1,3])[n%3]]
    make(SUBJECTS[area],topic,stem+' 소수 둘째 자리까지 계산하고 그 아래는 일반 반올림한다.',f'{fmt(result)} {unit}',[f'{fmt(x)} {unit}' for x in wrong],explanation+f' 계산 결과는 {fmt(result)} {unit}이다. 이상화한 학습 계산이며 장비 설명서·하중표·실제 안전거리의 대체값이 아니다.',len(bank)+1,'FL-'+kind,dict(kind=kind,values=values,result=float(result),unit=unit,precision=2))
# 주행: 단위·시간·기하. 조건마다 값이 달라지며 무작위 생성은 없다.
family(0,'speed','속도 단위 환산','m/s',lambda n:([n+3],f'지게차의 속도 표시가 {n+3} km/h이다. 이 속도는 몇 m/s인가?',D(n+3)/D('3.6'),f'1 km=1000 m, 1 h=3600 s이다. 따라서 속도=(km/h 값)÷3.6= {n+3}÷3.6 m/s.'))
family(0,'distance','등속 이동거리','m',lambda n:([n+5,12],f'학습 모형에서 지게차가 {n+5} m/min의 일정한 속도로 12분 움직인다. 이동거리는?',(n+5)*12,f'등속 이동거리=속도×시간. 단위 m/min과 min을 곱하므로 {n+5}×12 m로 계산한다.'))
family(0,'travelTime','이동 시간','s',lambda n:([3*(n+10),D('1.5').__float__()],f'일정한 속도 1.5 m/s로 {3*(n+10)} m를 이동하는 데 걸리는 시간은?',D(3*(n+10))/D('1.5'),f'시간=거리÷속도. {3*(n+10)} m÷1.5 m/s로 계산하면 초 단위를 얻는다. 가감속 시간은 제외한다.'))
family(0,'grade','경사도 계산','%',lambda n:([n,200],f'학습용 경사로의 수평거리 200 m에 대해 높이 차가 {n} m이다. 높이 차÷수평거리×100으로 정의한 경사도는?',D(n)/200*100,f'경사도(%)=높이 차/수평거리×100. {n}÷200×100으로 구한다. 이 계산은 장비의 등판 허용 여부를 뜻하지 않는다.'))
family(0,'wheelTravel','바퀴 회전과 거리','m',lambda n:([D('1.5').__float__(),n+10],f'미끄럼 없이 구르는 바퀴의 둘레가 1.5 m이다. {n+10}회전한 이동거리는?',D('1.5')*(n+10),f'바퀴 1회전에 둘레만큼 이동한다. 거리=둘레×회전수=1.5×{n+10} m이다.'))
family(0,'reaction','반응거리','m',lambda n:([n+2,D('0.8').__float__()],f'단순 학습 모형에서 속도 {n+2} km/h, 운전자 반응시간 0.8초이다. 제동 시작 전 반응거리는?',D(n+2)/D('3.6')*D('.8'),f'속도를 {n+2}÷3.6 m/s로 환산한 뒤 반응시간 0.8 s를 곱한다. 반응거리=v×t이며 제동거리와는 구별한다.'))
# 화물 적재: 중량·무게중심·이론 모멘트. 실제 허용하중 산정은 금지한다.
family(1,'grossMass','총 취급중량','kg',lambda n:([20+n,24,30],f'개당 {20+n} kg인 상자 24개와 30 kg 팔레트를 함께 든다. 총 취급중량은?',(20+n)*24+30,f'총중량=상자 1개 무게×개수+팔레트 무게. ({20+n}×24)+30 kg으로 계산한다.'))
family(1,'boxMass','균등 상자 중량','kg',lambda n:([(20+n)*16+25,25,16],f'팔레트 포함 총중량은 {(20+n)*16+25} kg, 팔레트는 25 kg이다. 같은 무게의 상자 16개가 실려 있다. 상자 1개의 무게는?',n+20,f'포장 등 추가 무게가 없다는 조건이다. 상자 총중량에서 팔레트 중량을 빼고 16으로 나눈다. ({(20+n)*16+25}-25)÷16 kg.'))
family(1,'moment','단순 하중 모멘트','kg·m',lambda n:([600+20*n,D('.6').__float__()],f'이론 계산에서 질량 {600+20*n} kg과 기준점까지의 수평거리 0.6 m의 곱을 구한다. 하중 모멘트 지표는?',D(600+20*n)*D('.6'),f'여기서는 질량×거리 지표를 사용하므로 단위는 kg·m이며 N·m 토크가 아니다. {600+20*n}×0.6을 계산한다. 실제 정격은 하중표로 판단한다.'))
family(1,'equivalentMass','이상 모멘트 등가','kg',lambda n:([800+20*n,D('.5').__float__(),D('.8').__float__()],f'순수한 학습 모형에서 {800+20*n} kg×0.5 m와 같은 질량·거리 곱을 만들려 한다. 거리가 0.8 m이면 등가 질량은? 실제 허용하중을 묻는 문제가 아니다.',D(800+20*n)*D('.5')/D('.8'),f'이상 모멘트 등가식 m₁d₁=m₂d₂를 사용한다. m₂={800+20*n}×0.5÷0.8 kg이다. 이 비례식으로 실제 지게차 허용하중을 결정하면 안 된다.'))
family(1,'center','합성 무게중심','m',lambda n:([100+10*n,D('.4').__float__(),200,D('1.0').__float__()],f'질량 {100+10*n} kg의 중심은 기준점에서 0.4 m, 질량 200 kg의 중심은 같은 방향으로 1.0 m이다. 받침 무게는 무시한다. 합성 중심의 거리는?',(D(100+10*n)*D('.4')+D(200))/(D(100+10*n)+200),f'같은 기준점에 대한 질량 가중평균을 구한다. x=({100+10*n}×0.4+200×1.0)÷({100+10*n}+200) m이다.'))
family(1,'loadRatio','명시된 한도 대비 비율','%',lambda n:([300+20*n,1500],f'어떤 작업 조건에 대한 하중표 한도가 이미 1500 kg으로 확인되었다. 총 취급중량이 {300+20*n} kg일 때 한도 대비 중량 비율은?',D(300+20*n)/1500*100,f'비율=취급중량÷확인된 한도×100. {300+20*n}÷1500×100%이다. 비율만으로 다른 작업 조건의 적합성까지 판단하지 않는다.'))
# 운반: 경로 계획을 위한 이상화 계산.
family(2,'cycleTime','운반 사이클 시간','min',lambda n:([4+n,2,3],f'한 운반 사이클은 주행 {4+n}분, 적재 2분, 하역 3분이다. 서로 겹치지 않으면 총 시간은?',n+9,f'순차 작업의 시간은 합한다. {4+n}+2+3 min이다. 대기나 휴식 등 명시되지 않은 시간은 포함하지 않는 학습 조건이다.'))
family(2,'throughput','시간당 운반량','kg/h',lambda n:([100+n*10,6],f'1회당 {100+n*10} kg를 운반하고 한 사이클이 6분이다. 1시간 동안 대기 없이 같은 작업을 반복할 때 운반량은?',(100+n*10)*10,f'시간당 사이클 수=60÷6=10회/h. 운반량={100+n*10}×10 kg/h이다. 작업 속도나 무리한 생산량을 권장하는 값은 아니다.'))
family(2,'roundTrip','왕복 주행거리','m',lambda n:([30+n,8],f'편도 {30+n} m 경로를 같은 길로 8회 왕복한다. 주행거리 합계는?',2*(30+n)*8,f'1회 왕복은 편도의 두 배이다. 총 거리=2×{30+n}×8 m. 경로 밖 이동은 없다고 가정한다.'))
family(2,'averageSpeed','평균 이동속도','m/min',lambda n:([200+n*10,10],f'정지 시간을 포함한 10분 동안 총 {200+n*10} m를 이동했다. 평균 이동속도는?',D(200+n*10)/10,f'평균속도는 총 이동거리÷전체 시간이다. {200+n*10}÷10 m/min으로 계산한다. 순간속도나 현장 제한속도와 구별한다.'))
family(2,'fuel','연료 사용량','L',lambda n:([D(10+n).__float__()/10,4],f'학습 모형에서 시간당 연료 사용량이 {D(10+n)/10} L/h로 일정하다. 4시간 사용량은?',D(10+n)/10*4,f'사용량=시간당 사용량×시간. {D(10+n)/10} L/h×4 h를 계산한다. 실제 소비는 운전 조건에 따라 달라진다.'))
family(2,'remainingTime','잔여 작업시간','min',lambda n:([120+n*2,45],f'작업에 사용할 수 있는 총 시간은 {120+n*2}분이다. 이미 45분을 사용했다. 남은 시간은?',75+n*2,f'잔여 시간=전체 가용 시간-경과 시간. {120+n*2}-45 min이다. 휴식이나 별도 제한시간이 없다는 산술 연습이다.'))
# 하역: 유압/일/동력 기초. 기계 효율·동하중 제외를 명시한다.
family(3,'pressure','유압 압력','MPa',lambda n:([10000+n*1000,5000],f'마찰을 무시한 직동 유압 실린더에 힘 {10000+n*1000} N, 유효면적 5000 mm²가 주어진다. 필요한 압력은?',D(10000+n*1000)/5000,f'p=F/A. 1 N/mm²=1 MPa이므로 {10000+n*1000}÷5000 MPa이다. 실제 장비 압력 조정값이 아니다.'))
family(3,'cylinderForce','유압 실린더 힘','N',lambda n:([D(10+n).__float__()/10,4000],f'직동 실린더의 유효면적 4000 mm²에 압력 {D(10+n)/10} MPa가 작용한다. 마찰·배압을 무시한 이론 힘은?',D(10+n)/10*4000,f'F=pA이다. 1 MPa=1 N/mm²이므로 {D(10+n)/10}×4000 N. 마스트 체인 배율 등의 영향은 없는 직접 실린더의 힘이다.'))
family(3,'oilVolume','실린더 체적','L',lambda n:([4000,100+n*10],f'유효면적 4000 mm²인 실린더가 {100+n*10} mm 이동한다. 단면적이 일정할 때 유입 체적은?',D(4000)*(100+n*10)/1000000,f'V=A×이동거리. 1 L=1,000,000 mm³이므로 4000×{100+n*10}÷1,000,000 L. 누설과 압축은 무시한다.'))
family(3,'fillTime','체적과 유량','s',lambda n:([D(10+n).__float__()/10,12],f'실린더에 필요한 체적은 {D(10+n)/10} L, 일정한 공급 유량은 12 L/min이다. 누설을 무시하면 채우는 데 몇 초 걸리는가?',D(10+n)/10/12*60,f'시간=체적÷유량. {D(10+n)/10}÷12 min을 얻은 뒤 60을 곱해 s로 환산한다.'))
family(3,'liftWork','인상에 필요한 일','J',lambda n:([100+n*10,2,10],f'질량 {100+n*10} kg의 화물을 수직으로 2 m 높인다. 중력가속도 g=10 m/s², 손실 무시 조건에서 한 일은?',(100+n*10)*2*10,f'중력에 대항한 일 W=mgh. {100+n*10} kg×10 m/s²×2 m로 계산하면 J이다. 가속 및 마찰에 필요한 일은 제외한다.'))
family(3,'liftPower','이상 인상동력','W',lambda n:([100+n*10,2,10,5],f'질량 {100+n*10} kg를 5초 동안 2 m 높인다. g=10 m/s², 손실을 무시한 평균 인상동력은?',D(100+n*10)*2*10/5,f'일 W=mgh, 평균동력 P=W/t. {100+n*10}×10×2÷5 W로 계산한다. 엔진·모터 실제 입력 정격이 아니다.'))
# 안전관리: 안전수치를 주장하지 않는 단순 물리·기하 연습.
family(4,'braking','이상 제동거리','m',lambda n:([D(10+n).__float__()/10,2],f'단순 등감속 모형에서 초기 속도 {D(10+n)/10} m/s, 감속도 크기 2 m/s²이다. 반응거리를 제외한 정지까지 제동거리는?',(D(10+n)/10)**2/4,f'v²=2as이므로 s=v²/(2a). ({D(10+n)/10})²÷(2×2) m이다. 실제 안전거리 기준이 아니며 노면과 적재 영향은 모형에서 제외했다.'))
family(4,'stopping','이상 총정지거리','m',lambda n:([D(10+n).__float__()/10,1,2],f'학습 모형의 초기 속도 {D(10+n)/10} m/s, 반응시간 1초, 이후 일정한 감속도 2 m/s²이다. 반응거리와 제동거리의 합은?',D(10+n)/10+(D(10+n)/10)**2/4,f'반응거리=vt={D(10+n)/10}×1 m. 제동거리=v²/(2a)=({D(10+n)/10})²÷4 m. 두 값을 합한다. 실제 안전거리로 사용하지 않는다.'))
family(4,'kinetic','운동에너지','J',lambda n:([1000+n*100,2],f'차량과 화물의 총질량이 {1000+n*100} kg, 속도가 2 m/s일 때 병진 운동에너지는?',D(1000+n*100)*4/2,f'운동에너지 E=½mv². 0.5×{1000+n*100}×2² J로 계산한다. 바퀴 회전 에너지 등은 제외한 학습 모형이다.'))
family(4,'heightGap','수직 치수 차','cm',lambda n:([300+n,280],f'출입구 높이가 {300+n} cm, 장비와 화물을 포함한 전체 높이가 280 cm이다. 두 높이의 단순 차이는? 안전한 통과 가능 여부를 묻는 것은 아니다.',20+n,f'높이 차=출입구 높이-전체 높이={300+n}-280 cm. 실제 통과 판단에는 노면, 흔들림, 장비 변형 및 별도 안전 여유 검토가 필요하다.'))
family(4,'widthGap','폭의 단순 여유','cm',lambda n:([200+n*2,160],f'직선 통로 폭이 {200+n*2} cm, 화물을 포함한 폭은 160 cm이다. 정확히 중앙에 있는 기하 모형에서 한쪽의 여유는?',D(40+n*2)/2,f'양쪽 여유 합=통로 폭-화물 폭. 중앙 배치이므로 한쪽 여유=({200+n*2}-160)÷2 cm. 실제 운행 가능한 통로 폭을 정하는 기준은 아니다.'))
family(4,'averageFloor','평균 면적하중 지표','kg/m²',lambda n:([1000+n*100,4],f'질량 {1000+n*100} kg가 면적 4 m²에 균등하게 분포한다고 가정한다. 평균 면적하중 지표는? 실제 지게차 바퀴의 집중하중 검토가 아니다.',D(1000+n*100)/4,f'평균 질량/면적 지표={1000+n*100}÷4 kg/m². 압력의 SI 단위 Pa와는 다르다. 실제 바닥 적합성은 바퀴 집중하중 등 별도 구조 검토가 필요하다.'))
assert len(bank)==1000
assert len({q['id'] for q in bank})==1000
for s in SUBJECTS:assert sum(q['subject']==s for q in bank)==200
(ROOT/'src/data/questions-main.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
example=dict(bank[0],id='LOCAL-TEMPLATE-001',question='새 문항을 여기에 작성하세요. 기본 예제를 그대로 승인하지 마세요.',verificationStatus='pending',reviewNote='출처·권리·정답 검수 후 승인')
(ROOT/'public/templates/questions.json').write_text(json.dumps([example],ensure_ascii=False,indent=2)+'\n')
choices=example.pop('choices')
for i,c in enumerate(choices,1):example['choice'+str(i)]=c
with (ROOT/'public/templates/questions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=example.keys());w.writeheader();w.writerow(example)
print('1000 authored questions: 100 concepts + 30 families × 30 variants; 200 per learning area')
