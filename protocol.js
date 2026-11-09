export function range(v,min,max,name='Value'){v=Number(v);if(!Number.isInteger(v)||v<min||v>max)throw Error(`${name}: ${min}–${max}`);return v}
export function duration(v){v=Number(v);if(!Number.isFinite(v)||v<0.2||v>10)throw Error('Duration: 0.2–10 seconds');return v}
export function packet(id,cmd,params=[]){range(id,0,254,'Servo ID');range(cmd,0,255,'Command');const data=[id,params.length+3,cmd,...params];if(data[1]>255)throw Error('Packet too long');return Uint8Array.from([85,85,...data,(~data.reduce((a,b)=>a+b,0))&255])}
export function u16(n){return [n&255,(n>>8)&255]}
export function position(id,pos,ms){range(pos,0,1000,'Position');range(ms,20,30000,'Move time');return packet(id,1,[...u16(pos),...u16(ms)])}
export function mode(id,m,speed=0){range(speed,-1000,1000,'Speed');return packet(id,29,[m,0,...u16(speed)])}
export function parseFrames(buffer){const frames=[];while(buffer.length>=2){let i=buffer.findIndex((v,j)=>v===85&&buffer[j+1]===85);if(i<0){buffer.splice(0,buffer.at(-1)===85?buffer.length-1:buffer.length);break}if(i)buffer.splice(0,i);if(buffer.length<4)break;let length=buffer[3];if(length<3||length>64){buffer.shift();continue}let size=length+3;if(buffer.length<size)break;let f=buffer.slice(0,size),check=(~f.slice(2,-1).reduce((a,b)=>a+b,0))&255;if(check!==f.at(-1)){buffer.shift();continue}buffer.splice(0,size);frames.push({id:f[2],cmd:f[4],params:f.slice(5,-1)})}return frames}
const addr=id=>String(range(id,0,255,'Motor ID')).padStart(3,'0');
export function drive(id,pwm,time=0){range(pwm,500,2500,'PWM');range(time,0,9999,'Time');return `#${addr(id)}P${String(pwm).padStart(4,'0')}T${String(time).padStart(4,'0')}!`}
export function command(id,suffix){if(!/^[A-Z0-9]+$/.test(suffix))throw Error('Invalid command');return `#${addr(id)}P${suffix}!`}
export function changeId(oldId,newId){range(newId,0,254,'New ID');return `#${addr(oldId)}PID${addr(newId)}!`}
export function wheelMix(mode,name){const patterns={forward:[1,1,1,1],back:[-1,-1,-1,-1],left:[-1,1,1,-1],right:[1,-1,-1,1],strafeLeft:[-1,1,-1,1],strafeRight:[1,-1,1,-1]};if(!patterns[name]||(mode==='normal'&&name.startsWith('strafe')))throw Error('Invalid drive pattern');return patterns[name]}
