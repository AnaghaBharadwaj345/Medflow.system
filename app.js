const initialPatients = [
  {id:'PT-1042', name:'Maya Thompson', age:34, urgency:'Critical', arrival:'07:42 AM', needs:'ICU bed, Doctor', wait:18, assigned:'ICU-04'},
  {id:'PT-1041', name:'James Wilson', age:67, urgency:'Urgent', arrival:'07:38 AM', needs:'Bed, Nurse', wait:22, assigned:'Ward B-12'},
  {id:'PT-1040', name:'Sofia Rodriguez', age:28, urgency:'Urgent', arrival:'07:31 AM', needs:'Operating room', wait:29, assigned:'OR-02'},
  {id:'PT-1039', name:'Noah Williams', age:51, urgency:'Moderate', arrival:'07:25 AM', needs:'Bed, Doctor', wait:35, assigned:'Pending'},
  {id:'PT-1038', name:'Emma Davis', age:42, urgency:'Moderate', arrival:'07:18 AM', needs:'Bed, Nurse', wait:42, assigned:'Ward A-07'},
  {id:'PT-1037', name:'Liam Brown', age:76, urgency:'Urgent', arrival:'07:11 AM', needs:'ICU bed, Nurse', wait:49, assigned:'ICU-02'},
  {id:'PT-1036', name:'Olivia Miller', age:19, urgency:'Low', arrival:'07:05 AM', needs:'Doctor', wait:55, assigned:'Pending'},
  {id:'PT-1035', name:'Ethan Moore', age:63, urgency:'Moderate', arrival:'06:58 AM', needs:'Bed, Nurse', wait:62, assigned:'Ward B-04'}
];
const resources = [
  {name:'General beds', icon:'▣', used:42, total:60, color:'blue'}, {name:'ICU beds', icon:'♥', used:8, total:10, color:'red'},
  {name:'Operating rooms', icon:'⊕', used:3, total:5, color:'purple'}, {name:'Doctors', icon:'♙', used:18, total:24, color:'green'},
  {name:'Nurses', icon:'♧', used:61, total:72, color:'orange'}, {name:'Emergency vehicles', icon:'▱', used:4, total:6, color:'cyan'}
];
let patients = structuredClone(initialPatients), elapsed=0, running=false, timer;
const $ = id => document.getElementById(id);
function urgencyClass(u){return u.toLowerCase()}
function renderQueue(){
  $('queueBody').innerHTML=patients.map(p=>`<tr><td><div class="patient"><div class="patient-avatar">${p.name.split(' ').map(x=>x[0]).join('')}</div><div><b>${p.name}</b><small>${p.id} · ${p.age} yrs</small></div></div></td><td><span class="badge ${urgencyClass(p.urgency)}"><i></i>${p.urgency}</span></td><td>${p.arrival}</td><td>${p.needs}</td><td><strong class="wait ${p.wait>45?'long':''}">${p.wait} min</strong></td><td><span class="assigned ${p.assigned==='Pending'?'pending':''}">${p.assigned==='Pending'?'◌ ': '✓ '}${p.assigned}</span></td><td><button class="row-menu">•••</button></td></tr>`).join('');
  $('navQueue').textContent=patients.length; $('waitingMetric').textContent=patients.length; $('criticalMetric').textContent=patients.filter(p=>p.urgency==='Critical').length; $('queueSummary').textContent=`Showing ${patients.length} of ${patients.length} patients`;
}
function renderResources(){ $('resourceList').innerHTML=resources.map(r=>{let pct=Math.round(r.used/r.total*100);return `<div class="resource"><div class="resource-top"><span class="resource-name"><i class="resource-icon ${r.color}">${r.icon}</i><b>${r.name}</b></span><span><strong>${r.used}</strong> / ${r.total}</span></div><div class="progress"><i class="${r.color}" style="width:${pct}%"></i></div><small>${pct}% utilized · ${r.total-r.used} available</small></div>`}).join('');}
function addActivity(text, icon='✓', type='success'){ $('activityFeed').insertAdjacentHTML('afterbegin',`<div class="activity-row"><span class="activity-icon ${type}">${icon}</span><div><b>${text}</b><small>Just now</small></div></div>`); if($('activityFeed').children.length>3)$('activityFeed').lastElementChild.remove(); }
function toast(msg){$('toast').textContent=msg;$('toast').classList.add('show');setTimeout(()=>$('toast').classList.remove('show'),2800)}
function updateClock(){elapsed++;let mins=elapsed, hour=8+Math.floor(mins/60), minute=mins%60;$('simTime').textContent=`${String(hour).padStart(2,'0')}:${String(minute).padStart(2,'0')} ${hour>=12?'PM':'AM'}`;$('simDay').textContent=`Day 1 · ${mins} min elapsed`;patients.forEach(p=>p.wait++);if(elapsed%3===0)renderQueue();}
$('runBtn').addEventListener('click',()=>{running=!running;$('runBtn').innerHTML=running?'Ⅱ Pause simulation':'▶ Run simulation';$('runBtn').classList.toggle('running',running);if(running){timer=setInterval(updateClock,1000);addActivity('Simulation started — processing patient arrivals','▶','info');toast('Simulation is running');}else{clearInterval(timer);addActivity('Simulation paused by operator','Ⅱ','info');toast('Simulation paused');}});
$('resetBtn').addEventListener('click',()=>{clearInterval(timer);running=false;elapsed=0;patients=structuredClone(initialPatients);$('runBtn').innerHTML='▶ Run simulation';$('runBtn').classList.remove('running');$('simTime').textContent='08:00 AM';$('simDay').textContent='Day 1 · 0 min elapsed';renderQueue();addActivity('Simulation reset to initial conditions','↻','info');toast('Simulation reset');});
$('addPatientBtn').addEventListener('click',()=>{const names=['Ava Johnson','Daniel Lee','Mia Taylor','Lucas Martin'];const name=names[Math.floor(Math.random()*names.length)];patients.unshift({id:'PT-'+(1043+patients.length),name,age:Math.floor(18+Math.random()*65),urgency:'Urgent',arrival:'Now',needs:'Bed, Doctor',wait:0,assigned:'Pending'});renderQueue();addActivity(`${name} added to the patient queue`,'+','info');toast('New patient added to queue');});
$('applyStrategy').addEventListener('click',()=>{const strategy=document.querySelector('input[name="strategy"]:checked').value;const values={urgency:['22 min','84%'],balanced:['16 min','91%'],utilization:['19 min','96%']};$('projectedWait').textContent=values[strategy][0];$('throughput').textContent=values[strategy][1];addActivity(`${strategy[0].toUpperCase()+strategy.slice(1)} scheduling strategy applied`,'⚙','info');toast('Scheduling strategy updated');});
$('activityFeed').innerHTML='';addActivity('ICU-04 allocated to Maya Thompson');addActivity('Emergency vehicle EV-02 returned to base','↩','info');addActivity('Staff shortage alert resolved in Ward B','✓','success');renderQueue();renderResources();
