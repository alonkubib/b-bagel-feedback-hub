#!/usr/bin/env python3
"""
Feedback Hub — Multi-tenant customer feedback management platform.
Features: review import, action tracking, email workflow, mystery shopper,
multi-account system with email-based login, paste-and-extract for
authenticated platforms (Deliveroo, TripAdvisor).
"""

import json, os

# Load data
with open('all_complaints.json','r') as f:
    complaints = json.load(f)
with open('all_compliments.json','r') as f:
    compliments = json.load(f)

complaint_json = json.dumps(complaints, ensure_ascii=False)
compliment_json = json.dumps(compliments, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Feedback Hub</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap');
:root{
  --bg:#f2f0ed;--surface:#ffffff;--surface2:#f8f7f5;--surface3:#edecea;
  --oak:#c4a882;--oak-dark:#a08660;--oak-light:#f0e8dd;
  --red:#d4372c;--red-soft:#fdecea;--red-dark:#b02a21;
  --steel:#8a9199;--steel-light:#e8ebed;
  --text:#1c1917;--text2:#78716c;--text3:#a8a29e;
  --green:#16a34a;--green-soft:#dcfce7;--amber:#d97706;--amber-soft:#fef3c7;
  --blue:#2563eb;--blue-soft:#dbeafe;
  --border:#e7e5e4;--border2:#d6d3d1;
  --r:14px;--r-sm:10px;--r-lg:20px;--r-full:999px;
  --sh:0 1px 2px rgba(0,0,0,.04),0 2px 8px rgba(0,0,0,.03);
  --sh-md:0 2px 8px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.04);
  --sh-lg:0 4px 12px rgba(0,0,0,.08),0 16px 48px rgba(0,0,0,.06);
  --font:'DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --t:all .2s cubic-bezier(.4,0,.2,1);
}
*{margin:0;padding:0;box-sizing:border-box}
html{font-size:16px;-webkit-text-size-adjust:100%}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.5;min-height:100vh;overflow-x:hidden}
button{cursor:pointer;font-family:inherit;border:none;background:none;font-size:inherit}
input,select,textarea{font-family:inherit;font-size:inherit}
a{text-decoration:none;color:inherit}
.app{display:flex;flex-direction:column;min-height:100vh}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;z-index:200;background:var(--surface);border-top:1px solid var(--border);display:flex;padding:6px 8px calc(6px + env(safe-area-inset-bottom));gap:2px}
.bottom-nav .nav-item{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 4px;border-radius:var(--r-sm);color:var(--text3);font-size:10px;font-weight:500;transition:var(--t);-webkit-tap-highlight-color:transparent}
.bottom-nav .nav-item.active{color:var(--red)}
.bottom-nav .nav-item svg{width:22px;height:22px}
.sidebar{display:none}
.main{flex:1;padding:16px 16px 90px;width:100%;max-width:100%}
@media(min-width:768px){
  .app{flex-direction:row}
  .bottom-nav{display:none}
  .sidebar{display:flex;flex-direction:column;width:240px;min-width:240px;background:var(--text);color:#fff;position:fixed;top:0;left:0;bottom:0;z-index:100;overflow-y:auto}
  .main{margin-left:240px;padding:28px 32px;max-width:calc(100% - 240px)}
}
@media(min-width:1200px){.main{padding:32px 48px}}
.sidebar-logo{padding:28px 24px 24px;display:flex;align-items:center;gap:14px;border-bottom:1px solid rgba(255,255,255,.08)}
.logo-mark{width:42px;height:42px;border-radius:50%;background:var(--red);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;color:#fff;flex-shrink:0}
.logo-text h1{font-size:16px;font-weight:700;letter-spacing:-.4px}
.logo-text span{font-size:11px;color:rgba(255,255,255,.4);display:block;margin-top:1px}
.sidebar-nav{flex:1;padding:20px 0}
.sidebar .nav-section{padding:0 24px;margin:24px 0 8px;font-size:10px;text-transform:uppercase;letter-spacing:1.4px;color:rgba(255,255,255,.25);font-weight:600}
.sidebar .nav-item{display:flex;align-items:center;gap:12px;padding:10px 24px;color:rgba(255,255,255,.55);font-size:13px;font-weight:500;transition:var(--t);border-left:3px solid transparent}
.sidebar .nav-item:hover{color:#fff;background:rgba(255,255,255,.04)}
.sidebar .nav-item.active{color:#fff;background:rgba(255,255,255,.08);border-left-color:var(--red)}
.sidebar .nav-item svg{width:18px;height:18px;opacity:.6;flex-shrink:0}
.sidebar .nav-item.active svg{opacity:1}
.nav-badge{margin-left:auto;background:var(--red);color:#fff;font-size:10px;padding:2px 7px;border-radius:10px;font-weight:700}
.page-header{margin-bottom:24px}
.page-header h2{font-size:22px;font-weight:700;letter-spacing:-.5px;color:var(--text)}
.page-header p{font-size:13px;color:var(--text2);margin-top:2px}
@media(min-width:768px){.page-header h2{font-size:26px}}
.card{background:var(--surface);border-radius:var(--r);border:1px solid var(--border);padding:20px;transition:var(--t)}
.card:hover{box-shadow:var(--sh)}
.kpi-grid{display:grid;gap:12px;grid-template-columns:repeat(2,1fr)}
@media(min-width:768px){.kpi-grid{grid-template-columns:repeat(4,1fr);gap:16px}}
.kpi{background:var(--surface);border-radius:var(--r);border:1px solid var(--border);padding:16px 18px;transition:var(--t)}
.kpi:hover{box-shadow:var(--sh)}
.kpi-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.8px;color:var(--text3);margin-bottom:8px}
.kpi-value{font-size:26px;font-weight:800;letter-spacing:-1px;color:var(--text);line-height:1.1}
.kpi-sub{font-size:11px;color:var(--text2);margin-top:4px;display:flex;align-items:center;gap:4px}
.kpi-up{color:var(--green)}.kpi-down{color:var(--red)}
.time-bar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:20px}
.time-chip{padding:7px 16px;border-radius:var(--r-full);font-size:12px;font-weight:600;background:var(--surface);border:1px solid var(--border);color:var(--text2);transition:var(--t);white-space:nowrap}
.time-chip:hover{border-color:var(--border2);color:var(--text)}
.time-chip.active{background:var(--text);color:#fff;border-color:var(--text)}
.chart-wrap{background:var(--surface);border-radius:var(--r);border:1px solid var(--border);padding:20px;margin-bottom:16px}
.chart-title{font-size:13px;font-weight:700;color:var(--text);margin-bottom:16px;display:flex;align-items:center;gap:8px}
.review-card{background:var(--surface);border-radius:var(--r);border:1px solid var(--border);padding:16px;margin-bottom:10px;transition:var(--t)}
.review-card:hover{box-shadow:var(--sh)}
.review-card.flagged{border-left:3px solid var(--red);background:var(--red-soft)}
.review-header{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:8px}
.review-meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.badge{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:var(--r-full);font-size:10px;font-weight:600;letter-spacing:.3px}
.badge-location{background:var(--oak-light);color:var(--oak-dark)}
.badge-source{background:var(--steel-light);color:var(--steel)}
.badge-type{background:var(--surface2);color:var(--text2);border:1px solid var(--border)}
.badge-urgent{background:var(--red);color:#fff}
.badge-complaint{background:var(--red-soft);color:var(--red)}
.badge-compliment{background:var(--green-soft);color:var(--green)}
.review-date{font-size:11px;color:var(--text3);white-space:nowrap;flex-shrink:0}
.review-text{font-size:13px;color:var(--text);line-height:1.65;margin-bottom:10px;cursor:pointer}
.review-text.truncated{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.review-customer{font-size:11px;color:var(--text3)}
.suggestion-box{margin-top:12px;padding:14px 16px;background:var(--surface2);border:1px solid var(--border);border-radius:var(--r-sm)}
.suggestion-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--amber);margin-bottom:4px;display:flex;align-items:center;gap:5px}
.suggestion-text{font-size:12px;color:var(--text2);line-height:1.5;margin-bottom:10px}
.suggestion-actions{display:flex;flex-wrap:wrap;gap:6px}
@media(max-width:767px){.suggestion-area{display:none}}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:8px 18px;border-radius:var(--r-full);font-size:13px;font-weight:600;transition:var(--t);white-space:nowrap}
.btn-primary{background:var(--red);color:#fff}.btn-primary:hover{background:var(--red-dark)}
.btn-secondary{background:var(--surface);border:1px solid var(--border);color:var(--text)}.btn-secondary:hover{border-color:var(--border2);background:var(--surface2)}
.btn-sm{padding:6px 14px;font-size:11px}
/* Action button states */
.btn-action{background:var(--oak-light);color:var(--oak-dark);border:1px solid var(--oak);font-size:11px;padding:5px 12px;border-radius:var(--r-full);font-weight:600;display:inline-flex;align-items:center;gap:4px;transition:var(--t)}
.btn-action:hover{background:var(--oak);color:#fff}
.btn-action.sending{background:var(--amber-soft);border-color:var(--amber);color:var(--amber);pointer-events:none}
.btn-action.sent{background:var(--green-soft);border-color:var(--green);color:var(--green);cursor:pointer}
.btn-action.sent:hover{background:var(--green);color:#fff}
.btn-action.replied{background:var(--blue-soft);border-color:var(--blue);color:var(--blue);cursor:pointer}
.btn-action.replied:hover{background:var(--blue);color:#fff}
.btn-action svg{width:12px;height:12px}
.filter-bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.filter-select{padding:8px 14px;border-radius:var(--r-full);border:1px solid var(--border);background:var(--surface);font-size:12px;font-weight:500;color:var(--text);outline:none;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2378716c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;padding-right:32px;cursor:pointer}
.filter-input{padding:8px 14px;border-radius:var(--r-full);border:1px solid var(--border);background:var(--surface);font-size:12px;color:var(--text);outline:none;min-width:0;flex:1;max-width:260px}
.filter-input:focus,.filter-select:focus{border-color:var(--red);box-shadow:0 0 0 3px var(--red-soft)}
.toggle-group{display:inline-flex;border:1px solid var(--border);border-radius:var(--r-full);overflow:hidden;background:var(--surface)}
.toggle-btn{padding:7px 16px;font-size:12px;font-weight:600;color:var(--text2);transition:var(--t)}
.toggle-btn.active{background:var(--text);color:#fff}
.pagination{display:flex;align-items:center;justify-content:center;gap:8px;padding:20px 0}
.page-btn{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;border:1px solid var(--border);background:var(--surface);color:var(--text2);transition:var(--t)}
.page-btn:hover{border-color:var(--border2)}.page-btn.active{background:var(--text);color:#fff;border-color:var(--text)}.page-btn:disabled{opacity:.3;cursor:default}
.info-icon{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:50%;background:var(--steel-light);color:var(--steel);font-size:11px;font-weight:700;cursor:help;position:relative;flex-shrink:0}
.info-tooltip{display:none;position:absolute;bottom:calc(100% + 10px);left:50%;transform:translateX(-50%);width:280px;background:var(--text);color:#fff;padding:14px 16px;border-radius:var(--r-sm);font-size:12px;font-weight:400;line-height:1.6;z-index:999;pointer-events:none;box-shadow:var(--sh-lg)}
.info-tooltip::after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:6px solid transparent;border-top-color:var(--text)}
.info-icon:hover .info-tooltip,.info-icon:focus .info-tooltip{display:block}
.score-input{width:60px;padding:8px;border:1px solid var(--border);border-radius:var(--r-sm);text-align:center;font-weight:700;font-size:16px;outline:none}
.score-input:focus{border-color:var(--red);box-shadow:0 0 0 3px var(--red-soft)}
.int-card{background:var(--surface);border-radius:var(--r);border:1px solid var(--border);padding:20px;display:flex;align-items:flex-start;gap:16px;margin-bottom:12px;transition:var(--t)}
.int-card:hover{box-shadow:var(--sh)}
.int-icon{width:44px;height:44px;border-radius:var(--r-sm);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;flex-shrink:0}
.int-body{flex:1;min-width:0}
.int-name{font-size:14px;font-weight:700;margin-bottom:2px}
.int-desc{font-size:12px;color:var(--text2);line-height:1.5;margin-bottom:10px}
.int-status{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600}
.int-connected{color:var(--green)}.int-disconnected{color:var(--text3)}
.int-steps{margin-top:10px;padding:12px;background:var(--surface2);border-radius:var(--r-sm);font-size:12px;color:var(--text2);line-height:1.7}
.int-steps ol{padding-left:18px}
.digest-layout{display:flex;flex-direction:column;gap:20px}
@media(min-width:900px){.digest-layout{flex-direction:row}}
.digest-config{flex:1;min-width:0}.digest-preview{flex:1;min-width:0;max-width:100%}
.digest-preview-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:24px;font-size:13px;line-height:1.7}
.switch{position:relative;width:42px;height:24px;background:var(--border2);border-radius:var(--r-full);cursor:pointer;transition:var(--t);flex-shrink:0}
.switch.on{background:var(--green)}
.switch::after{content:'';position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;transition:var(--t);box-shadow:0 1px 3px rgba(0,0,0,.2)}
.switch.on::after{left:21px}
.toast{position:fixed;top:20px;right:20px;z-index:600;background:var(--text);color:#fff;padding:12px 20px;border-radius:var(--r);font-size:13px;font-weight:500;box-shadow:var(--sh-lg);animation:slideIn .3s ease;display:flex;align-items:center;gap:8px;max-width:380px}
@keyframes slideIn{from{transform:translateY(-20px);opacity:0}to{transform:translateY(0);opacity:1}}
@keyframes spin{to{transform:rotate(360deg)}}
.spinner{width:14px;height:14px;border:2px solid var(--amber);border-top-color:transparent;border-radius:50%;animation:spin .6s linear infinite;display:inline-block}
/* Modal overlay */
.modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:500;display:flex;align-items:center;justify-content:center;padding:16px;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.modal-box{background:var(--surface);border-radius:var(--r-lg);box-shadow:var(--sh-lg);width:100%;max-width:560px;max-height:85vh;overflow-y:auto;animation:slideUp .3s ease}
@keyframes slideUp{from{transform:translateY(30px);opacity:0}to{transform:translateY(0);opacity:1}}
.modal-header{display:flex;align-items:center;justify-content:space-between;padding:20px 24px 16px;border-bottom:1px solid var(--border)}
.modal-header h3{font-size:16px;font-weight:700}
.modal-close{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--surface2);color:var(--text2);font-size:18px;transition:var(--t)}
.modal-close:hover{background:var(--border);color:var(--text)}
.modal-body{padding:24px}
/* Calendar overlay */
.cal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.4);z-index:500;display:flex;align-items:center;justify-content:center;padding:16px}
.cal-box{background:var(--surface);border-radius:var(--r-lg);box-shadow:var(--sh-lg);padding:24px;width:100%;max-width:360px}
.cal-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.cal-header button{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid var(--border);background:var(--surface);color:var(--text)}
.cal-header button:hover{background:var(--surface2)}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;text-align:center}
.cal-day-name{font-size:10px;font-weight:600;color:var(--text3);padding:6px 0;text-transform:uppercase}
.cal-day{padding:8px 4px;font-size:13px;border-radius:var(--r-sm);cursor:pointer;transition:var(--t);font-weight:500}
.cal-day:hover{background:var(--surface2)}
.cal-day.today{font-weight:700;color:var(--red)}
.cal-day.in-range{background:var(--red-soft);color:var(--red)}
.cal-day.range-start,.cal-day.range-end{background:var(--red);color:#fff;font-weight:700}
.cal-day.other-month{color:var(--text3)}
.cal-day.disabled{opacity:.3;pointer-events:none}
.rank-bar{height:8px;border-radius:4px;transition:width .5s ease}
.rank-row{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border)}
.rank-row:last-child{border-bottom:none}
.rank-num{width:28px;height:28px;border-radius:50%;background:var(--surface2);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}
.rank-num.gold{background:var(--amber-soft);color:var(--amber)}
.rank-num.silver{background:var(--steel-light);color:var(--steel)}
.rank-num.bronze{background:var(--oak-light);color:var(--oak-dark)}
/* Email thread in modal */
.email-block{padding:16px;border:1px solid var(--border);border-radius:var(--r-sm);margin-bottom:12px}
.email-block.outgoing{background:var(--surface2);border-left:3px solid var(--red)}
.email-block.incoming{background:var(--green-soft);border-left:3px solid var(--green)}
.email-meta{font-size:11px;color:var(--text3);margin-bottom:8px;display:flex;flex-wrap:wrap;gap:8px}
.email-meta strong{color:var(--text)}
.email-body{font-size:13px;line-height:1.7;color:var(--text)}
/* Action log timeline */
.action-timeline{position:relative;padding-left:20px;margin-top:12px}
.action-timeline::before{content:'';position:absolute;left:6px;top:4px;bottom:4px;width:2px;background:var(--border)}
.timeline-item{position:relative;padding:6px 0 6px 16px;font-size:12px;color:var(--text2)}
.timeline-item::before{content:'';position:absolute;left:-17px;top:10px;width:10px;height:10px;border-radius:50%;background:var(--green);border:2px solid var(--surface)}
.timeline-item.pending::before{background:var(--border2)}
/* Swipe area */
.swipe-area{touch-action:pan-y;user-select:none;-webkit-user-select:none}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
.flex{display:flex}.items-center{align-items:center}.justify-between{justify-content:space-between}.gap-2{gap:8px}.gap-3{gap:12px}
.mt-2{margin-top:8px}.mt-3{margin-top:12px}.mt-4{margin-top:16px}.mb-2{margin-bottom:8px}.mb-3{margin-bottom:12px}
.text-sm{font-size:13px}.text-xs{font-size:11px}.font-bold{font-weight:700}.text-muted{color:var(--text2)}.text-light{color:var(--text3)}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
@media(max-width:500px){.grid-2{grid-template-columns:1fr}}
</style>
</head>
<body>
<div id="root"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.6/babel.min.js"></script>
<script type="text/babel">
const {useState,useEffect,useMemo,useRef,useCallback,createContext,useContext}=React;

const COMPLAINT_DATA = ''' + complaint_json + r''';
const COMPLIMENT_DATA = ''' + compliment_json + r''';

/* ═══ MULTI-TENANT ACCOUNT SYSTEM ═══ */
const ACCT_STORAGE='fhub_accounts';
const SESSION_STORAGE='fhub_session';
const API_BASE='https://feedback.agarden.cloud';
async function apiFetch(path,opts={}){
  const session=loadSession();
  const headers={'Content-Type':'application/json',...(opts.headers||{})};
  if(session&&session.email)headers['X-User-Email']=session.email;
  else if(session&&session.accountId)headers['X-Account-Id']=session.accountId;
  const resp=await fetch(API_BASE+path,{...opts,headers});
  if(!resp.ok){const err=await resp.json().catch(()=>({error:'Request failed'}));throw new Error(err.error||'API error '+resp.status)}
  return resp.json();
}
const COLORS_POOL=['#d4372c','#2563eb','#7c3aed','#16a34a','#d97706','#0891b2','#be185d','#e11d48','#0d9488','#7c2d12'];

/* B Bagel — Alon's pre-configured account */
const BBAGEL_ACCOUNT={
  id:'bbagel',
  businessName:'B Bagel',
  feedbackEmail:'feedback@bbagel.co.uk',
  adminEmails:['yoav@bbagel.co.uk','rachel@bbagel.co.uk','alonkubi@gmail.com'],
  locations:[
    {id:'fulham',name:'Fulham',address:'236D Fulham Rd, SW10 9NB',color:'#d4372c',openedDate:'2019-03-01'},
    {id:'soho',name:'Soho',address:'18 Wardour St, W1D 6QJ',color:'#2563eb',openedDate:'2020-06-01'},
    {id:'tcr',name:'TCR',address:'Tottenham Court Road',color:'#7c3aed',openedDate:'2021-04-01'},
    {id:'camden',name:'Camden',address:'Camden High St, NW1',color:'#16a34a',openedDate:'2022-02-01'},
    {id:'strand',name:'Strand',address:'The Strand, WC2R',color:'#d97706',openedDate:'2023-01-01'},
    {id:'swains',name:'Swains Lane',address:'Swains Lane, N6',color:'#0891b2',openedDate:'2023-06-01'},
    {id:'nos',name:'New Oxford St',address:'52 New Oxford St, WC1A 1ES',color:'#be185d',openedDate:'2025-10-01'},
  ],
  users:[
    {id:'u1',name:'Yoav',email:'yoav@bbagel.co.uk',role:'Admin'},
    {id:'u2',name:'Rachel',email:'rachel@bbagel.co.uk',role:'Admin'},
    {id:'u3',name:'Alon',email:'alonkubi@gmail.com',role:'Admin'},
  ],
  hasEmbeddedData:true
};

function loadAccounts(){
  try{const d=JSON.parse(localStorage.getItem(ACCT_STORAGE));if(d&&d.length)return d}catch(e){}
  const init=[BBAGEL_ACCOUNT];localStorage.setItem(ACCT_STORAGE,JSON.stringify(init));return init;
}
function saveAccounts(accts){localStorage.setItem(ACCT_STORAGE,JSON.stringify(accts))}
function loadSession(){try{return JSON.parse(localStorage.getItem(SESSION_STORAGE))}catch(e){return null}}
function saveSession(s){localStorage.setItem(SESSION_STORAGE,JSON.stringify(s))}
function clearSession(){localStorage.removeItem(SESSION_STORAGE)}
function findAccountByEmail(email){
  const e=email.toLowerCase().trim();
  const accts=loadAccounts();
  return accts.find(a=>a.adminEmails.some(ae=>ae.toLowerCase()===e));
}

/* Account context */
const AccountCtx=createContext(null);
function useAccount(){return useContext(AccountCtx)}

/* ═══ BIBLICAL LOGO SVG ═══ */
function FeedbackHubLogo({size=42,light=false}){
  const fg=light?'#fff':'#1c1917';
  return React.createElement('svg',{width:size,height:size,viewBox:'0 0 48 48',fill:'none',xmlns:'http://www.w3.org/2000/svg'},
    React.createElement('rect',{width:48,height:48,rx:12,fill:'#d4372c'}),
    React.createElement('path',{d:'M12 10c0-1 .8-2 2-2h14c1.5 0 3 1 4 2l4 5c.6.8 1 1.8 1 2.8V38c0 1.1-.9 2-2 2H14c-1.1 0-2-.9-2-2V10z',fill:'#fff',opacity:.9}),
    React.createElement('path',{d:'M28 8v8c0 .6.4 1 1 1h6',fill:'none',stroke:'#d4372c',strokeWidth:1.5,strokeLinecap:'round'}),
    React.createElement('path',{d:'M17 22h14M17 27h14M17 32h10',stroke:'#d4372c',strokeWidth:1.8,strokeLinecap:'round',opacity:.6}),
    React.createElement('path',{d:'M19 15l2.5 2L25 13',fill:'none',stroke:'#d4372c',strokeWidth:2,strokeLinecap:'round',strokeLinejoin:'round'}),
  );
}

/* ═══ LOGIN SCREEN ═══ */
function LoginScreen({onLogin}){
  const [email,setEmail]=useState('');
  const [mode,setMode]=useState('login');/* login | signup */
  const [bizName,setBizName]=useState('');
  const [err,setErr]=useState('');
  const [loading,setLoading]=useState(false);

  const handleLogin=async()=>{
    if(!email.trim()){setErr('Enter your email address');return}
    setLoading(true);setErr('');
    try{
      const resp=await fetch(API_BASE+'/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email.toLowerCase().trim()})});
      if(resp.ok){
        const d=await resp.json();
        const localAcct={id:d.id,businessName:d.name,feedbackEmail:d.adminEmails[0]||email.toLowerCase().trim(),adminEmails:d.adminEmails,locations:d.locations||[],users:[{id:'u1',name:email.split('@')[0],email:email.toLowerCase().trim(),role:'Admin'}],hasEmbeddedData:d.id==='bbagel'};
        const accts=loadAccounts();const idx=accts.findIndex(a=>a.id===localAcct.id);
        if(idx>=0)accts[idx]={...accts[idx],...localAcct};else accts.push(localAcct);
        saveAccounts(accts);
        saveSession({accountId:localAcct.id,email:email.toLowerCase().trim()});
        onLogin();
      }else{
        const acct=findAccountByEmail(email);
        if(acct){saveSession({accountId:acct.id,email:email.toLowerCase().trim()});onLogin()}
        else{setErr('No account found for this email. Create a new account below.');setMode('signup')}
      }
    }catch(e){
      const acct=findAccountByEmail(email);
      if(acct){saveSession({accountId:acct.id,email:email.toLowerCase().trim()});onLogin()}
      else{setErr('Cannot connect to server. Please try again.')}
    }finally{setLoading(false)}
  };
  const handleSignup=async()=>{
    if(!email.trim()||!bizName.trim()){setErr('Fill in all fields');return}
    setLoading(true);setErr('');
    try{
      const resp=await fetch(API_BASE+'/api/accounts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:bizName.trim(),email:email.toLowerCase().trim()})});
      if(resp.ok){
        const d=await resp.json();
        const newAcct={id:d.id,businessName:d.name,feedbackEmail:email.toLowerCase().trim(),adminEmails:d.adminEmails,locations:d.locations||[],users:[{id:'u1',name:email.split('@')[0],email:email.toLowerCase().trim(),role:'Admin'}],hasEmbeddedData:false};
        const accts=loadAccounts();accts.push(newAcct);saveAccounts(accts);
        saveSession({accountId:d.id,email:email.toLowerCase().trim()});
        onLogin();
      }else if(resp.status===409){setErr('An account with this email already exists')}
      else{const err=await resp.json().catch(()=>({}));setErr(err.error||'Signup failed')}
    }catch(e){
      const accts=loadAccounts();
      if(accts.find(a=>a.adminEmails.some(ae=>ae.toLowerCase()===email.toLowerCase().trim()))){setErr('An account with this email already exists');setLoading(false);return}
      const id='acct_'+Date.now();
      const newAcct={id,businessName:bizName.trim(),feedbackEmail:email.toLowerCase().trim(),adminEmails:[email.toLowerCase().trim()],locations:[],users:[{id:'u1',name:email.split('@')[0],email:email.toLowerCase().trim(),role:'Admin'}],hasEmbeddedData:false};
      accts.push(newAcct);saveAccounts(accts);
      saveSession({accountId:id,email:email.toLowerCase().trim()});
      onLogin();
    }finally{setLoading(false)}
  };

  return React.createElement('div',{style:{minHeight:'100vh',background:'linear-gradient(135deg,#1c1917 0%,#292524 50%,#1c1917 100%)',display:'flex',alignItems:'center',justifyContent:'center',padding:20}},
    React.createElement('div',{style:{maxWidth:420,width:'100%',textAlign:'center'}},
      React.createElement('div',{style:{marginBottom:32}},
        React.createElement(FeedbackHubLogo,{size:64}),
        React.createElement('h1',{style:{color:'#fff',fontSize:28,fontWeight:800,marginTop:16,letterSpacing:'-0.5px'}},'Feedback Hub'),
        React.createElement('p',{style:{color:'rgba(255,255,255,.5)',fontSize:14,marginTop:4}},'Customer feedback management platform')
      ),
      React.createElement('div',{style:{background:'#fff',borderRadius:16,padding:32,boxShadow:'0 8px 32px rgba(0,0,0,.3)'}},
        mode==='login'?React.createElement(React.Fragment,null,
          React.createElement('h2',{style:{fontSize:18,fontWeight:700,marginBottom:4}},'Sign In'),
          React.createElement('p',{style:{fontSize:13,color:'#78716c',marginBottom:20}},'Enter your admin email to access your account'),
          React.createElement('input',{type:'email',value:email,onChange:e=>{setEmail(e.target.value);setErr('')},onKeyDown:e=>e.key==='Enter'&&handleLogin(),placeholder:'your@email.com',style:{width:'100%',padding:'12px 16px',border:'1px solid #e7e5e4',borderRadius:10,fontSize:14,marginBottom:12,outline:'none',fontFamily:'var(--font)'}}),
          err&&React.createElement('div',{style:{color:'#d4372c',fontSize:12,marginBottom:12}},err),
          React.createElement('button',{onClick:handleLogin,disabled:loading,style:{width:'100%',padding:'12px',background:loading?'#999':'#d4372c',color:'#fff',border:'none',borderRadius:10,fontSize:14,fontWeight:700,cursor:loading?'wait':'pointer',fontFamily:'var(--font)'}},loading?'Signing in...':'Sign In'),
          React.createElement('div',{style:{marginTop:16,paddingTop:16,borderTop:'1px solid #e7e5e4'}},
            React.createElement('p',{style:{fontSize:12,color:'#a8a29e'}},"Don't have an account? "),
            React.createElement('button',{onClick:()=>{setMode('signup');setErr('')},style:{color:'#d4372c',fontWeight:600,fontSize:13,cursor:'pointer',background:'none',border:'none',fontFamily:'var(--font)'}},'Create one free')
          )
        ):React.createElement(React.Fragment,null,
          React.createElement('h2',{style:{fontSize:18,fontWeight:700,marginBottom:4}},'Create Account'),
          React.createElement('p',{style:{fontSize:13,color:'#78716c',marginBottom:20}},'Set up your business in 30 seconds'),
          React.createElement('input',{type:'text',value:bizName,onChange:e=>{setBizName(e.target.value);setErr('')},placeholder:'Your business name',style:{width:'100%',padding:'12px 16px',border:'1px solid #e7e5e4',borderRadius:10,fontSize:14,marginBottom:12,outline:'none',fontFamily:'var(--font)'}}),
          React.createElement('input',{type:'email',value:email,onChange:e=>{setEmail(e.target.value);setErr('')},onKeyDown:e=>e.key==='Enter'&&handleSignup(),placeholder:'Admin email address',style:{width:'100%',padding:'12px 16px',border:'1px solid #e7e5e4',borderRadius:10,fontSize:14,marginBottom:12,outline:'none',fontFamily:'var(--font)'}}),
          err&&React.createElement('div',{style:{color:'#d4372c',fontSize:12,marginBottom:12}},err),
          React.createElement('button',{onClick:handleSignup,style:{width:'100%',padding:'12px',background:'#d4372c',color:'#fff',border:'none',borderRadius:10,fontSize:14,fontWeight:700,cursor:'pointer',fontFamily:'var(--font)'}},'Create Account'),
          React.createElement('div',{style:{marginTop:16,paddingTop:16,borderTop:'1px solid #e7e5e4'}},
            React.createElement('button',{onClick:()=>{setMode('login');setErr('')},style:{color:'#d4372c',fontWeight:600,fontSize:13,cursor:'pointer',background:'none',border:'none',fontFamily:'var(--font)'}},'← Back to sign in')
          )
        )
      )
    )
  );
}

/* ═══ PASTE & EXTRACT MODAL ═══ */
function PasteExtractModal({platform,locationId,onExtracted,onClose}){
  const [html,setHtml]=useState('');
  const [results,setResults]=useState(null);
  const [err,setErr]=useState('');

  const extractReviews=()=>{
    if(!html.trim()){setErr('Paste the page content first');return}
    setErr('');
    const reviews=[];
    const doc=new DOMParser().parseFromString(html,'text/html');
    if(platform==='deliveroo'){
      /* Deliveroo review patterns */
      const cards=doc.querySelectorAll('[class*="Review"],[class*="review"],[data-test-id*="review"]');
      cards.forEach(card=>{
        const text=card.querySelector('[class*="text"],[class*="comment"],[class*="body"]');
        const rating=card.querySelector('[class*="star"],[class*="rating"],[aria-label*="star"]');
        const date=card.querySelector('[class*="date"],[class*="time"]');
        const author=card.querySelector('[class*="name"],[class*="author"]');
        if(text&&text.textContent.trim()){
          let r=0;
          if(rating){const m=rating.textContent.match(/(\d)/)||rating.getAttribute('aria-label')?.match(/(\d)/);if(m)r=parseInt(m[1])}
          reviews.push({date:date?date.textContent.trim():new Date().toISOString().split('T')[0],rating:r||null,author:author?author.textContent.trim():'Deliveroo Customer',text:text.textContent.trim(),source:'Deliveroo'});
        }
      });
      /* Fallback: try to find text patterns */
      if(reviews.length===0){
        const allText=doc.body?doc.body.innerText||doc.body.textContent:'';
        const blocks=allText.split(/\n{2,}/);
        let current=null;
        blocks.forEach(b=>{
          const t=b.trim();
          if(t.length>20&&t.length<1000&&!t.includes('Deliveroo')&&!t.includes('menu')&&!t.includes('basket')){
            reviews.push({date:new Date().toISOString().split('T')[0],rating:null,author:'Deliveroo Customer',text:t,source:'Deliveroo'});
          }
        });
      }
    }else if(platform==='tripadvisor'){
      /* TripAdvisor review patterns */
      const cards=doc.querySelectorAll('[class*="review"],[data-test-target*="review"],.reviewSelector');
      cards.forEach(card=>{
        const text=card.querySelector('[class*="text"],[class*="entry"],[class*="partial_entry"],[class*="reviewText"],.entry');
        const bubble=card.querySelector('[class*="bubble"],[class*="rating"]');
        const date=card.querySelector('[class*="date"],[class*="ratingDate"]');
        const author=card.querySelector('[class*="username"],[class*="member"],.memberOverlayLink');
        if(text&&text.textContent.trim()){
          let r=0;
          if(bubble){const cls=bubble.className||'';const m=cls.match(/bubble_(\d)/);if(m)r=parseInt(m[1])}
          reviews.push({date:date?date.textContent.trim().replace(/.*Reviewed\s*/i,''):new Date().toISOString().split('T')[0],rating:r||null,author:author?author.textContent.trim():'TripAdvisor User',text:text.textContent.trim(),source:'TripAdvisor'});
        }
      });
    }
    if(reviews.length>0){setResults(reviews)}else{setErr('Could not extract reviews. Try selecting all content on the review page (Ctrl+A), copy (Ctrl+C), then paste here.')}
  };
  const saveReviews=()=>{
    if(!results||!results.length)return;
    onExtracted(results);
    onClose();
  };

  return React.createElement('div',{style:{position:'fixed',inset:0,zIndex:9999,background:'rgba(0,0,0,.5)',display:'flex',alignItems:'center',justifyContent:'center',padding:20},onClick:e=>e.target===e.currentTarget&&onClose()},
    React.createElement('div',{style:{background:'#fff',borderRadius:16,width:'100%',maxWidth:600,maxHeight:'80vh',overflow:'auto',padding:24}},
      React.createElement('div',{style:{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:16}},
        React.createElement('h3',{style:{fontSize:18,fontWeight:700}},'Paste & Extract — '+platform),
        React.createElement('button',{onClick:onClose,style:{fontSize:20,cursor:'pointer',background:'none',border:'none'}},'×')
      ),
      React.createElement('div',{style:{background:'#fef3c7',border:'1px solid #fbbf24',borderRadius:10,padding:12,marginBottom:16,fontSize:12}},
        React.createElement('strong',null,'How it works:'),' 1) Open the review page on '+platform+' in a new tab. 2) Log in if needed. 3) Select all (Ctrl+A), Copy (Ctrl+C). 4) Paste here (Ctrl+V). 5) Click Extract.'
      ),
      !results?React.createElement(React.Fragment,null,
        React.createElement('textarea',{value:html,onChange:e=>{setHtml(e.target.value);setErr('')},placeholder:'Paste the full page content here (Ctrl+V)...',style:{width:'100%',minHeight:200,padding:12,border:'1px solid #e7e5e4',borderRadius:10,resize:'vertical',fontFamily:'monospace',fontSize:11}}),
        err&&React.createElement('div',{style:{color:'#d4372c',fontSize:12,marginTop:8}},err),
        React.createElement('div',{style:{display:'flex',gap:8,marginTop:12}},
          React.createElement('button',{onClick:extractReviews,style:{padding:'10px 20px',background:'#d4372c',color:'#fff',border:'none',borderRadius:8,fontSize:13,fontWeight:600,cursor:'pointer'}},'Extract Reviews'),
          React.createElement('button',{onClick:onClose,style:{padding:'10px 20px',background:'#e7e5e4',color:'#1c1917',border:'none',borderRadius:8,fontSize:13,fontWeight:600,cursor:'pointer'}},'Cancel')
        )
      ):React.createElement(React.Fragment,null,
        React.createElement('div',{style:{background:'#dcfce7',border:'1px solid #86efac',borderRadius:10,padding:12,marginBottom:12,fontSize:13,fontWeight:600,color:'#16a34a'}},'Found '+results.length+' reviews!'),
        React.createElement('div',{style:{maxHeight:300,overflow:'auto',marginBottom:12}},
          results.slice(0,5).map((r,i)=>React.createElement('div',{key:i,style:{padding:10,background:'#f8f7f5',borderRadius:8,marginBottom:6,fontSize:12}},
            React.createElement('div',{style:{fontWeight:600}},r.author+(r.rating?' — '+r.rating+'/5':'')),
            React.createElement('div',{style:{color:'#78716c',marginTop:2}},r.text.substring(0,150)+(r.text.length>150?'...':''))
          )),
          results.length>5&&React.createElement('div',{style:{fontSize:12,color:'#78716c',textAlign:'center',padding:8}},'...and '+(results.length-5)+' more')
        ),
        React.createElement('div',{style:{display:'flex',gap:8}},
          React.createElement('button',{onClick:saveReviews,style:{padding:'10px 20px',background:'#16a34a',color:'#fff',border:'none',borderRadius:8,fontSize:13,fontWeight:600,cursor:'pointer'}},'Import '+results.length+' Reviews'),
          React.createElement('button',{onClick:()=>{setResults(null);setHtml('')},style:{padding:'10px 20px',background:'#e7e5e4',color:'#1c1917',border:'none',borderRadius:8,fontSize:13,fontWeight:600,cursor:'pointer'}},'Try Again')
        )
      )
    )
  );
}

/* ═══ LOCATIONS (now dynamic from account) ═══ */
const BBAGEL_LOCATIONS=[
  {id:'fulham',name:'Fulham',address:'236D Fulham Rd, SW10 9NB',color:'#d4372c',openedDate:'2019-03-01'},
  {id:'soho',name:'Soho',address:'18 Wardour St, W1D 6QJ',color:'#2563eb',openedDate:'2020-06-01'},
  {id:'tcr',name:'TCR',address:'Tottenham Court Road',color:'#7c3aed',openedDate:'2021-04-01'},
  {id:'camden',name:'Camden',address:'Camden High St, NW1',color:'#16a34a',openedDate:'2022-02-01'},
  {id:'strand',name:'Strand',address:'The Strand, WC2R',color:'#d97706',openedDate:'2023-01-01'},
  {id:'swains',name:'Swains Lane',address:'Swains Lane, N6',color:'#0891b2',openedDate:'2023-06-01'},
  {id:'nos',name:'New Oxford St',address:'52 New Oxford St, WC1A 1ES',color:'#be185d',openedDate:'2025-10-01'},
];
/* LOCATIONS is set dynamically from account — default to B Bagel for backwards compat */
let LOCATIONS=BBAGEL_LOCATIONS;

function monthsOpen(openedStr, refDate){
  const opened=new Date(openedStr);
  const ref=refDate||new Date();
  const m=(ref.getFullYear()-opened.getFullYear())*12+(ref.getMonth()-opened.getMonth());
  return Math.max(1,m);
}

const URGENT_WORDS=['food poisoning','poisoning','hospital','ambulance','allergy','allergic','anaphyl','sick','vomit','nhs','a&e','glass','metal','insect','hair in','cockroach','mouse','rat','racist','assault','threat','police','lawyer','legal','lawsuit','health inspector','trading standards','fsa'];
const IMPORTANT_WORDS=['refund','compensation','never coming back','worst','disgusting','horrible','terrible','unacceptable','manager','rude','dirty','hygiene','mould','mold','expire','raw','undercooked','cold food'];

function flagReview(text){if(!text)return null;const t=text.toLowerCase();if(URGENT_WORDS.some(w=>t.includes(w)))return 'urgent';if(IMPORTANT_WORDS.some(w=>t.includes(w)))return 'important';return null}

/* ═══ AI ACTION ENGINE ═══
   Analyses each review and suggests the best response action.
   Additional actions are suggested based on content. */
/* Helper: get current account info */
function getCurrentAccount(){
  const s=loadSession();if(!s)return BBAGEL_ACCOUNT;
  const accts=loadAccounts();return accts.find(a=>a.id===s.accountId)||BBAGEL_ACCOUNT;
}
function getBusinessName(){return getCurrentAccount().businessName||'My Business'}
function getFeedbackEmail(){return getCurrentAccount().feedbackEmail||'feedback@example.com'}

/* ═══ MYSTERY SHOPPER QUESTIONS (editable in Settings) ═══ */
const DEFAULT_MYSTERY_CATS=[
  {id:'clean',name:'Cleanliness',w:15,questions:['Are tables and surfaces clean?','Are floors swept and mopped?','Are toilets clean and stocked?']},
  {id:'friendly',name:'Staff Friendliness',w:15,questions:['Were you greeted on arrival?','Did staff smile and make eye contact?','Was the goodbye friendly?']},
  {id:'accuracy',name:'Order Accuracy',w:15,questions:['Was your order correct?','Were any items missing?','Were special requests honoured?']},
  {id:'quality',name:'Food Quality',w:15,questions:['Was the food fresh?','Was it prepared to standard?','Was the temperature correct?']},
  {id:'wait',name:'Wait Time',w:10,questions:['How long did you wait to order?','How long for food?']},
  {id:'present',name:'Presentation',w:10,questions:['Was food presented well?','Was packaging neat (if takeaway)?']},
  {id:'allergen',name:'Allergen Info',w:10,questions:['Were allergen signs visible?','Could staff answer allergen questions?']},
  {id:'overall',name:'Overall Experience',w:10,questions:['Would you return?','Would you recommend to a friend?']},
];

/* ═══ DEFAULT USERS & PERMISSIONS ═══ */
const BBAGEL_USERS=[
  {id:'u1',name:'Yoav',email:'yoav@bbagel.co.uk',role:'Admin',permissions:{dashboard:true,reviews:true,report:true,locations:true,mystery:true,integrations:true,digest:true,settings:true},locationAccess:'all'},
  {id:'u2',name:'Rachel',email:'rachel@bbagel.co.uk',role:'Admin',permissions:{dashboard:true,reviews:true,report:true,locations:true,mystery:true,integrations:true,digest:true,settings:true},locationAccess:'all'},
  {id:'u3',name:'Alon',email:'alonkubi@gmail.com',role:'Admin',permissions:{dashboard:true,reviews:true,report:true,locations:true,mystery:true,integrations:true,digest:true,settings:true},locationAccess:'all'},
];
function getDefaultUsers(acct){
  if(acct&&acct.id==='bbagel')return BBAGEL_USERS;
  if(acct&&acct.users)return acct.users.map((u,i)=>({id:'u'+(i+1),...u,permissions:{dashboard:true,reviews:true,report:true,locations:true,mystery:true,integrations:true,digest:true,settings:true},locationAccess:'all'}));
  return [];
}
const DEFAULT_USERS=BBAGEL_USERS;

const FEATURE_LIST=[
  {id:'dashboard',label:'Dashboard'},
  {id:'reviews',label:'Reviews'},
  {id:'report',label:'Report'},
  {id:'locations',label:'Performance'},
  {id:'mystery',label:'Mystery Shopper'},
  {id:'integrations',label:'Integrations'},
  {id:'digest',label:'Email Digest'},
  {id:'settings',label:'Settings'},
];

/* ═══ REVIEW IMPORT ENGINE ═══
   Fetches reviews from public platforms via a Google Apps Script proxy.
   Stores config in localStorage, imported reviews in localStorage too.
   Merges imported reviews with embedded data on every render.
*/

const REVIEW_PLATFORMS=[
  {id:'google',name:'Google Reviews',icon:'G',color:'#4285f4',bg:'#e8f0fe',fieldLabel:'Google Place ID',fieldPlaceholder:'e.g. ChIJ...  (from Google Maps URL)',fieldHelp:'Find your Place ID at: https://developers.google.com/maps/documentation/places/web-service/place-id',public:true},
  {id:'trustpilot',name:'Trustpilot',icon:'T',color:'#00b67a',bg:'#e0f5ed',fieldLabel:'Trustpilot Business URL',fieldPlaceholder:'e.g. https://www.trustpilot.com/review/bbagel.co.uk',fieldHelp:'Your Trustpilot business page URL',public:true},
  {id:'tripadvisor',name:'TripAdvisor',icon:'TA',color:'#34e0a1',bg:'#e3faf0',fieldLabel:'TripAdvisor URL',fieldPlaceholder:'e.g. https://www.tripadvisor.co.uk/Restaurant_Review-...',fieldHelp:'Your TripAdvisor listing page URL',public:true},
  {id:'deliveroo',name:'Deliveroo',icon:'D',color:'#00ccbc',bg:'#e0faf6',fieldLabel:'Deliveroo Store URL',fieldPlaceholder:'e.g. https://deliveroo.co.uk/menu/london/fulham/b-bagel-fulham',fieldHelp:'Your Deliveroo restaurant page URL. Requires login — click "Fetch" to open login window.',public:false},
  {id:'justeat',name:'Just Eat',icon:'J',color:'#f36d00',bg:'#fef0e5',fieldLabel:'Just Eat Restaurant URL',fieldPlaceholder:'e.g. https://www.just-eat.co.uk/restaurants-b-bagel-...',fieldHelp:'Your Just Eat restaurant listing URL',public:true},
];

/* Default review platform URLs for all B Bagel locations (pre-filled from public listings) */
const DEFAULT_LOCATION_URLS={
  fulham:{
    trustpilot:'https://uk.trustpilot.com/review/www.bbagel.co.uk',
    tripadvisor:'https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d9855458-Reviews-B_Bagel_Fulham-London_England.html',
    deliveroo:'https://deliveroo.co.uk/menu/london/chelsea/b-bagel-bakery'
  },
  soho:{
    trustpilot:'https://uk.trustpilot.com/review/www.bbagel.co.uk',
    tripadvisor:'https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d18935812-Reviews-B_Bagel_Soho-London_England.html',
    deliveroo:'https://deliveroo.co.uk/menu/london/soho/b-bagel-bakery-bar-soho'
  },
  tcr:{
    trustpilot:'https://uk.trustpilot.com/review/www.bbagel.co.uk',
    tripadvisor:'https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d23752937-Reviews-B_Bagel_Tottenham_Court_Road-London_England.html',
    deliveroo:'https://deliveroo.co.uk/menu/london/tottenham-court-road/b-bagel-bakery-bar-tottenham-court-road'
  },
  camden:{
    trustpilot:'https://uk.trustpilot.com/review/www.bbagel.co.uk',
    tripadvisor:'https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d26831811-Reviews-B_Bagel_Camden-London_England.html',
    deliveroo:'https://deliveroo.co.uk/menu/London/camden/b-bagel-camden'
  },
  strand:{
    trustpilot:'https://uk.trustpilot.com/review/www.bbagel.co.uk',
    tripadvisor:'https://www.tripadvisor.com/Restaurant_Review-g186338-d33011712-Reviews-B_Bagel_Strand-London_England.html',
    deliveroo:'https://deliveroo.co.uk/menu/london/strand/b-bagel-strand'
  },
  swains:{
    trustpilot:'https://uk.trustpilot.com/review/www.bbagel.co.uk',
    tripadvisor:'https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d33011707-Reviews-B_Bagel_Swain_s_Lane-London_England.html',
    deliveroo:'https://deliveroo.co.uk/menu/London/highgate/b-bagel-swains-lane'
  },
  nos:{
    trustpilot:'https://uk.trustpilot.com/review/www.bbagel.co.uk',
    deliveroo:'https://deliveroo.co.uk/menu/london/bloomsbury/b-bagel-new-oxford-street'
  }
};

/* Saved config shape in localStorage('fhub_{accountId}_sources'):
   { googleApiKey: '',
     locations: { fulham: { google: 'ChIJ...', trustpilot: 'https://...', ... }, ... },
     lastImport: { fulham: { google: '2026-03-10T...', ... }, ... }
   }
*/
function getStorageKey(suffix){const s=loadSession();const id=s?s.accountId:'bbagel';return 'fhub_'+id+'_'+suffix}

function getReviewConfig(){
  try{
    /* Try new key first, fall back to legacy */
    let saved=JSON.parse(localStorage.getItem(getStorageKey('sources')))||{};
    if(!saved.locations){const legacy=JSON.parse(localStorage.getItem('bbagel_review_sources'));if(legacy&&legacy.locations)saved=legacy}
    /* Auto-merge defaults for any locations missing URLs */
    if(!saved._defaultsMerged){
      if(!saved.locations) saved.locations={};
      Object.keys(DEFAULT_LOCATION_URLS).forEach(locId=>{
        if(!saved.locations[locId]) saved.locations[locId]={};
        Object.entries(DEFAULT_LOCATION_URLS[locId]).forEach(([platform,url])=>{
          if(!saved.locations[locId][platform]&&url) saved.locations[locId][platform]=url;
        });
      });
      saved._defaultsMerged=true;
      localStorage.setItem(getStorageKey('sources'),JSON.stringify(saved));
    }
    return saved;
  }catch(e){return{locations:JSON.parse(JSON.stringify(DEFAULT_LOCATION_URLS))}}
}
function saveReviewConfig(cfg){
  localStorage.setItem(getStorageKey('sources'),JSON.stringify(cfg));
}

/* Import reviews via server-side VPS API (replaces old Apps Script proxy) */
async function fetchReviewsViaServer(locations, googleApiKey, locationNames){
  const session=loadSession();
  if(!session||!session.email) return {ok:false,error:'Not logged in'};
  try{
    const data=await apiFetch('/api/fetch-reviews',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({locations,googleApiKey:googleApiKey||'',locationNames:locationNames||{}})});
    return {ok:true,...data};
  }catch(e){
    return {ok:false,error:e.message};
  }
}

/* Pull all reviews from server into localStorage for rendering */
async function syncReviewsFromServer(){
  const session=loadSession();
  if(!session||!session.email) return;
  try{
    const data=await apiFetch('/api/reviews?limit=5000');
    const existing=getImportedReviews();
    const allFingerprints=new Set();
    const embeddedComps=typeof COMPLIMENT_DATA!=='undefined'?COMPLIMENT_DATA:[];
    const embeddedComplaints=typeof COMPLAINT_DATA!=='undefined'?COMPLAINT_DATA:[];
    [...embeddedComps,...embeddedComplaints,...existing.complaints,...existing.compliments].forEach(r=>allFingerprints.add(reviewFingerprint(r)));
    let added=0;
    (data.reviews||[]).forEach(r=>{
      const review={location:r.location||'Unknown',date:r.date||'',source:r.platform||'unknown',type:r.category||'General',info:r.text||'',customer:r.author||'Anonymous',...(r.rating?{rating:r.rating}:{})};
      const fp=reviewFingerprint(review);
      if(!allFingerprints.has(fp)){
        allFingerprints.add(fp);
        if(r.sentiment==='positive'||r.type==='compliment'){existing.compliments.push(review)}
        else{existing.complaints.push({...review,action:'',manager:''})}
        added++;
      }
    });
    if(added>0) saveImportedReviews(existing);
    return added;
  }catch(e){console.error('syncReviewsFromServer error:',e);return 0}
}

/* Get all imported reviews from localStorage */
function getImportedReviews(){
  try{return JSON.parse(localStorage.getItem(getStorageKey('reviews')))||{complaints:[],compliments:[]}}catch(e){return{complaints:[],compliments:[]}}
}
function saveImportedReviews(data){
  localStorage.setItem(getStorageKey('reviews'),JSON.stringify(data));
}

/* Deduplicate by creating a fingerprint from date+source+info substring */
function reviewFingerprint(r){
  const info=(r.info||'').substring(0,60).toLowerCase().replace(/[^a-z0-9]/g,'');
  return (r.location||'')+'|'+(r.date||'')+'|'+(r.source||'')+'|'+info;
}

/* Merge fetched reviews into localStorage, avoiding duplicates. Also syncs to API. */
function mergeImportedReviews(newReviews, locationName, platformName){
  const existing=getImportedReviews();
  const allFingerprints=new Set();
  const apiQueue=[];

  /* Fingerprint embedded data too */
  const embeddedComps=typeof COMPLIMENT_DATA!=='undefined'?COMPLIMENT_DATA:[];
  const embeddedComplaints=typeof COMPLAINT_DATA!=='undefined'?COMPLAINT_DATA:[];
  [...embeddedComps,...embeddedComplaints,...existing.complaints,...existing.compliments].forEach(r=>allFingerprints.add(reviewFingerprint(r)));

  let added=0;
  newReviews.forEach(r=>{
    const review={
      location:locationName,
      date:r.date||new Date().toISOString().split('T')[0],
      source:platformName,
      type:r.type||'General',
      info:r.text||r.info||'',
      customer:r.author||r.customer||'Anonymous',
      ...(r.employee?{employee:r.employee}:{}),
      ...(r.rating!==undefined?{rating:r.rating}:{})
    };
    const fp=reviewFingerprint(review);
    if(!allFingerprints.has(fp)){
      allFingerprints.add(fp);
      /* Rating >= 4 or no rating = compliment; else complaint */
      const isCompliment=r.rating===undefined||r.rating>=4;
      if(isCompliment){
        existing.compliments.push(review);
      }else{
        existing.complaints.push({...review,action:'',manager:''});
      }
      apiQueue.push({platform:platformName||'unknown',author:review.customer||'Anonymous',rating:r.rating||null,text:review.info||'',date:review.date,location:locationName||null,type:isCompliment?'compliment':'complaint'});
      added++;
    }
  });

  saveImportedReviews(existing);
  /* Fire-and-forget API sync */
  if(apiQueue.length>0){try{const s=loadSession();if(s&&s.email){fetch(API_BASE+'/api/reviews/bulk',{method:'POST',headers:{'Content-Type':'application/json','X-User-Email':s.email},body:JSON.stringify({reviews:apiQueue})}).catch(()=>{})}}catch(e){}}
  return added;
}

/* Run full import via VPS server-side fetching (replaces old proxy-based import) */
async function runFullImport(onProgress){
  const cfg=getReviewConfig();
  const session=loadSession();
  if(!session||!session.email) return{total:0,errors:['Not logged in. Please sign in first.']};

  /* Build locations map + locationNames map for the server.
     Use the sources config directly (not LOCATIONS array) so ALL configured sources are included. */
  const locs=cfg.locations||{};
  const serverLocations={};
  const locationNames={};

  /* Build a name lookup from LOCATIONS array (UI-visible locations) */
  const locNameMap={};
  (typeof LOCATIONS!=='undefined'?LOCATIONS:[]).forEach(l=>{locNameMap[l.id]=l.name});

  for(const [locId,locCfg] of Object.entries(locs)){
    const hasAnySources=Object.values(locCfg).some(v=>v);
    if(hasAnySources){
      serverLocations[locId]={};
      locationNames[locId]=locNameMap[locId]||locId.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
      REVIEW_PLATFORMS.forEach(p=>{
        if(locCfg[p.id]) serverLocations[locId][p.id]=locCfg[p.id];
      });
    }
  }

  if(Object.keys(serverLocations).length===0) return{total:0,errors:['No review sources configured. Go to Settings → Review Sources to add platform URLs.']};

  if(onProgress) onProgress('Sending request to server...');

  /* Call server to fetch all reviews */
  const result=await fetchReviewsViaServer(serverLocations,cfg.googleApiKey,locationNames);

  if(!result.ok) return{total:0,errors:[result.error]};

  /* Now sync server reviews to localStorage for display */
  if(onProgress) onProgress('Syncing reviews to display...');
  await syncReviewsFromServer();

  /* Update last import timestamp */
  cfg.lastImport=cfg.lastImport||{};
  Object.keys(serverLocations).forEach(locId=>{
    cfg.lastImport[locId]=cfg.lastImport[locId]||{};
    Object.keys(serverLocations[locId]).forEach(platId=>{
      cfg.lastImport[locId][platId]=new Date().toISOString();
    });
  });
  saveReviewConfig(cfg);

  /* Also save sources to server */
  try{apiFetch('/api/account/sources',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({locations:serverLocations,googleApiKey:cfg.googleApiKey||'',locationNames})}).catch(()=>{})}catch(e){}

  return{total:result.total||0,errors:result.errors?result.errors.map(e=>e.location+'/'+e.platform+': '+e.error):[],details:result.details||[]};
}

const DEFAULT_ACTIONS=[
  {id:'respond',label:'Send Response',icon:'✉',always:true,removable:false},
  {id:'log_incident',label:'Log Incident',icon:'📋',keywords:['food poisoning','allergy','hospital','glass','metal','insect','sick','vomit','injury'],forType:'complaint'},
  {id:'refund',label:'Process Refund',icon:'💷',keywords:['refund','compensation','overcharged','wrong order','missing','charged twice'],forType:'complaint'},
  {id:'check_batch',label:'Check Batch',icon:'🔍',keywords:['mould','mold','expire','stale','raw','undercooked','off','spoiled','bad taste'],forType:'complaint'},
  {id:'staff_review',label:'Staff Review',icon:'👥',keywords:['rude','attitude','ignored','slow','unfriendly','unprofessional','manager'],forType:'complaint'},
  {id:'thank_team',label:'Thank Team',icon:'⭐',keywords:[],forType:'compliment'},
  {id:'share_social',label:'Share on Social',icon:'📱',keywords:['best','amazing','love','fantastic','brilliant','outstanding','perfect'],forType:'compliment'},
  {id:'loyalty_reward',label:'Loyalty Reward',icon:'🎁',keywords:['regular','always','every week','loyal','fan','favourite'],forType:'compliment'},
];

function suggestActions(item, type, enabledActions){
  const text=(item.info||item.customer_name||'').toLowerCase();
  const flag=flagReview(item.info);
  const actions=[];
  const available=enabledActions||DEFAULT_ACTIONS;

  /* Always add respond first */
  const respond=available.find(a=>a.id==='respond');
  if(respond)actions.push({...respond,primary:true});

  /* Add matching keyword actions */
  available.forEach(a=>{
    if(a.id==='respond')return;
    if(a.forType && a.forType!==type)return;
    if(a.keywords && a.keywords.length>0 && a.keywords.some(k=>text.includes(k))){
      actions.push(a);
    }
  });

  /* For urgent complaints, always add log_incident if not already there */
  if(flag==='urgent' && type==='complaint'){
    if(!actions.find(a=>a.id==='log_incident')){
      const li=available.find(a=>a.id==='log_incident');
      if(li)actions.splice(1,0,li);
    }
  }

  /* For compliments with no extra actions, add thank_team */
  if(type==='compliment' && actions.length===1){
    const tt=available.find(a=>a.id==='thank_team');
    if(tt)actions.push(tt);
  }

  return actions;
}

/* Generate email content for a review */
function generateEmail(item, type, actionId){
  const customerName=item.customer_name||'Valued Customer';
  const location=item.location||'';
  const date=item.date||'';
  const reviewText=(item.info||'').slice(0,200);
  const biz=getBusinessName();
  const femail=getFeedbackEmail();

  if(type==='complaint'){
    if(actionId==='refund'){
      return {
        subject: 'Your refund from '+biz+' '+location,
        from: femail,
        to: customerName,
        body: 'Dear '+customerName+',\n\nThank you for bringing this to our attention. We sincerely apologise for your experience at our '+location+' store.\n\nWe have reviewed your feedback and would like to offer you a full refund. Our team has been notified and we are taking steps to ensure this does not happen again.\n\nPlease reply to this email with your preferred refund method and we will process it within 2 business days.\n\nWith our apologies,\nThe '+biz+' Team\n'+femail
      };
    }
    return {
      subject: 'Re: Your feedback about '+biz+' '+location,
      from: femail,
      to: customerName,
      body: 'Dear '+customerName+',\n\nThank you for your feedback regarding your visit to our '+location+' store on '+date+'.\n\nWe are sorry to hear about your experience. We take all feedback seriously and your comments have been shared with our '+location+' team leader.\n\nWe would love the chance to make this right. Please do not hesitate to reply to this email or visit us again — your next coffee is on us.\n\nKind regards,\nThe '+biz+' Team\n'+femail
    };
  }
  return {
    subject: 'Thank you for your kind words! — '+biz+' '+location,
    from: femail,
    to: customerName,
    body: 'Dear '+customerName+',\n\nThank you so much for your lovely feedback about our '+location+' store! It truly means the world to our team.\n\nWe have shared your kind words with our '+location+' crew — it really made their day.\n\nWe look forward to welcoming you back soon!\n\nWarm regards,\nThe '+biz+' Team\n'+femail
  };
}

/* Simulated customer replies */
function simulateReply(email, type){
  const replies=[
    {delay:'2h',body:'Thank you for getting back to me so quickly. I appreciate it.'},
    {delay:'1d',body:'Thanks for the response. I would like a refund to my original payment method please.'},
    {delay:'4h',body:'That is very kind of you, thank you! We will definitely be back.'},
    {delay:'3h',body:'I appreciate the apology. Will give you another chance next week.'},
    {delay:'6h',body:'Thank you! Your team at the store is always so friendly.'},
  ];
  return replies[Math.floor(Math.random()*replies.length)];
}

/* ═══ HELPERS ═══ */
function parseDate(str){if(!str)return null;const parts=str.split(/[-\/]/);if(parts.length===3){if(parts[0].length===4)return new Date(+parts[0],+parts[1]-1,+parts[2]);return new Date(+parts[2],+parts[1]-1,+parts[0])}return new Date(str)}
function fmt(d){if(!d)return'';return d.toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'})}
function fmtTime(d){if(!d)return'';return d.toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'})}
function daysAgo(n){const d=new Date();d.setDate(d.getDate()-n);d.setHours(0,0,0,0);return d}
function lastWeekStart(){const d=new Date();const day=d.getDay();const diff=day===0?6:day-1;d.setDate(d.getDate()-diff-7);d.setHours(0,0,0,0);return d}
function lastWeekEnd(){const d=lastWeekStart();d.setDate(d.getDate()+6);d.setHours(23,59,59,999);return d}
function startOfMonth(){const d=new Date();d.setDate(1);d.setHours(0,0,0,0);return d}
function startOfLastMonth(){const d=new Date();d.setMonth(d.getMonth()-1);d.setDate(1);d.setHours(0,0,0,0);return d}
function endOfLastMonth(){const d=new Date();d.setDate(0);d.setHours(23,59,59,999);return d}
function fyStart(date){const d=date||new Date();return new Date(d.getMonth()>=3?d.getFullYear():d.getFullYear()-1,3,1)}
function fyEnd(date){const d=date||new Date();return new Date(d.getMonth()>=3?d.getFullYear()+1:d.getFullYear(),2,31,23,59,59,999)}
function fyLabel(date){const s=fyStart(date);return 'FY '+s.getFullYear()+'/'+(s.getFullYear()+1).toString().slice(2)}

/* ═══ ICONS ═══ */
const I={
  dashboard:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="4" rx="1"/><rect x="14" y="10" width="7" height="11" rx="1"/><rect x="3" y="13" width="7" height="8" rx="1"/></svg>,
  feed:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>,
  report:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>,
  trophy:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 9H4.5a2.5 2.5 0 010-5H6"/><path d="M18 9h1.5a2.5 2.5 0 000-5H18"/><path d="M4 22h16"/><path d="M10 22V8a6 6 0 0112 0v14"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/></svg>,
  mystery:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>,
  integrations:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>,
  digest:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>,
  settings:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>,
  bolt:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>,
  calendar:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="14" height="14"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>,
  camera:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="14" height="14"><path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/><circle cx="12" cy="13" r="4"/></svg>,
  upload:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="14" height="14"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0018 9h-1.26A8 8 0 103 16.3"/></svg>,
  mail:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="14" height="14"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>,
  check:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="12" height="12"><polyline points="20 6 9 17 4 12"/></svg>,
  reply:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="12" height="12"><polyline points="9 17 4 12 9 7"/><path d="M20 18v-2a4 4 0 00-4-4H4"/></svg>,
  clock:<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="12" height="12"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>,
};

const NAV=[
  {id:'dashboard',label:'Dashboard',icon:I.dashboard},
  {id:'reviews',label:'Reviews',icon:I.feed},
  {id:'report',label:'Report',icon:I.report},
  {id:'locations',label:'Performance',icon:I.trophy},
  {id:'mystery',label:'Mystery Shopper',icon:I.mystery},
  {id:'integrations',label:'Integrations',icon:I.integrations},
  {id:'digest',label:'Email Digest',icon:I.digest},
  {id:'settings',label:'Settings',icon:I.settings},
];

/* ═══ SHARED COMPONENTS ═══ */
function Toast({msg,onClose}){useEffect(()=>{const t=setTimeout(onClose,3500);return()=>clearTimeout(t)},[]);return <div className="toast">{msg}</div>}
function InfoIcon({text}){return <span className="info-icon" tabIndex={0}>?<span className="info-tooltip">{text}</span></span>}

function CalendarPicker({onSelect,onClose,initStart,initEnd}){
  const [viewDate,setViewDate]=useState(()=>new Date(initStart||new Date()));
  const [rangeStart,setRangeStart]=useState(initStart||null);
  const [rangeEnd,setRangeEnd]=useState(initEnd||null);
  const [selecting,setSelecting]=useState('start');
  const y=viewDate.getFullYear(),m=viewDate.getMonth();
  const firstDay=new Date(y,m,1).getDay()||7;
  const daysInMonth=new Date(y,m+1,0).getDate();
  const prevDays=new Date(y,m,0).getDate();
  const days=[];
  for(let i=firstDay-1;i>0;i--)days.push({d:prevDays-i+1,cur:false});
  for(let i=1;i<=daysInMonth;i++)days.push({d:i,cur:true});
  const rem=7-days.length%7;if(rem<7)for(let i=1;i<=rem;i++)days.push({d:i,cur:false});
  const today=new Date();
  const handleClick=(day)=>{
    if(!day.cur)return;
    const clicked=new Date(y,m,day.d);
    if(selecting==='start'){setRangeStart(clicked);setRangeEnd(null);setSelecting('end')}
    else{if(clicked<rangeStart){setRangeEnd(rangeStart);setRangeStart(clicked)}else{setRangeEnd(clicked)}setSelecting('start')}
  };
  const isInRange=(day)=>{if(!day.cur||!rangeStart||!rangeEnd)return false;const d=new Date(y,m,day.d);return d>rangeStart&&d<rangeEnd};
  const isStart=(day)=>{if(!day.cur||!rangeStart)return false;const d=new Date(y,m,day.d);return d.toDateString()===rangeStart.toDateString()};
  const isEnd=(day)=>{if(!day.cur||!rangeEnd)return false;const d=new Date(y,m,day.d);return d.toDateString()===rangeEnd.toDateString()};
  const isToday=(day)=>day.cur&&day.d===today.getDate()&&m===today.getMonth()&&y===today.getFullYear();
  const monthNames=['January','February','March','April','May','June','July','August','September','October','November','December'];
  return <div className="cal-overlay" onClick={onClose}><div className="cal-box" onClick={e=>e.stopPropagation()}>
    <div className="cal-header"><button onClick={()=>setViewDate(new Date(y,m-1,1))}>←</button><div style={{fontWeight:700,fontSize:14}}>{monthNames[m]} {y}</div><button onClick={()=>setViewDate(new Date(y,m+1,1))}>→</button></div>
    <div style={{fontSize:11,color:'var(--text3)',marginBottom:12,textAlign:'center'}}>
      {selecting==='start'?'Select start date':'Select end date'}
      {rangeStart&&<span> · From: {fmt(rangeStart)}</span>}
      {rangeEnd&&<span> · To: {fmt(rangeEnd)}</span>}
    </div>
    <div className="cal-grid">
      {['Mo','Tu','We','Th','Fr','Sa','Su'].map(d=><div key={d} className="cal-day-name">{d}</div>)}
      {days.map((day,i)=><div key={i} className={`cal-day${!day.cur?' other-month':''}${isToday(day)?' today':''}${isInRange(day)?' in-range':''}${isStart(day)?' range-start':''}${isEnd(day)?' range-end':''}`} onClick={()=>handleClick(day)}>{day.d}</div>)}
    </div>
    <div style={{display:'flex',gap:8,marginTop:16,justifyContent:'flex-end'}}>
      <button className="btn btn-sm btn-secondary" onClick={onClose}>Cancel</button>
      <button className="btn btn-sm btn-primary" disabled={!rangeStart||!rangeEnd} onClick={()=>{onSelect(rangeStart,rangeEnd);onClose()}}>Apply</button>
    </div>
  </div></div>;
}

/* ═══ EMAIL MODAL ═══ */
function EmailModal({emailData, onClose}){
  if(!emailData)return null;
  const {email, reply, actionLog, item, type}=emailData;
  return <div className="modal-overlay" onClick={onClose}><div className="modal-box" onClick={e=>e.stopPropagation()}>
    <div className="modal-header">
      <h3>📧 Action Details</h3>
      <button className="modal-close" onClick={onClose}>×</button>
    </div>
    <div className="modal-body">
      {/* Action timeline */}
      {actionLog&&actionLog.length>0&&<div style={{marginBottom:20}}>
        <div className="text-xs font-bold text-muted mb-2">ACTION LOG</div>
        <div className="action-timeline">
          {actionLog.map((a,i)=><div key={i} className={`timeline-item ${a.status||''}`}>
            <span className="font-bold">{a.action}</span> · <span className="text-light">{a.time}</span>
          </div>)}
        </div>
      </div>}

      {/* Original review */}
      <div style={{marginBottom:20}}>
        <div className="text-xs font-bold text-muted mb-2">ORIGINAL {type==='complaint'?'COMPLAINT':'COMPLIMENT'}</div>
        <div style={{padding:12,background:type==='complaint'?'var(--red-soft)':'var(--green-soft)',borderRadius:'var(--r-sm)',fontSize:13,lineHeight:1.6}}>
          <div className="text-xs font-bold mb-2">{item.location} · {item.date} · {item.source||'Website'}</div>
          {item.info||'No details'}
        </div>
      </div>

      {/* Sent email */}
      {email&&<div style={{marginBottom:16}}>
        <div className="text-xs font-bold text-muted mb-2">EMAIL SENT</div>
        <div className="email-block outgoing">
          <div className="email-meta">
            <span><strong>From:</strong> {email.from}</span>
            <span><strong>To:</strong> {email.to}</span>
          </div>
          <div className="text-xs font-bold mb-2">{email.subject}</div>
          <div className="email-body" style={{whiteSpace:'pre-line'}}>{email.body}</div>
        </div>
      </div>}

      {/* Reply */}
      {reply&&<div>
        <div className="text-xs font-bold text-muted mb-2">CUSTOMER REPLY</div>
        <div className="email-block incoming">
          <div className="email-meta">
            <span><strong>From:</strong> {item.customer_name||'Customer'}</span>
            <span><strong>Received:</strong> {reply.delay} later</span>
          </div>
          <div className="email-body">{reply.body}</div>
        </div>
      </div>}
      {!reply&&email&&<div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)',textAlign:'center'}}>
        <div className="text-xs text-muted">No reply received yet</div>
      </div>}
    </div>
  </div></div>;
}

/* ═══ REVIEW CARD with smart actions ═══ */
function ReviewCard({item, type, enabledActions, actionStates, setActionStates, setToast, setEmailModal}){
  const flag=flagReview(item.info);
  const [expanded,setExpanded]=useState(false);
  const reviewKey=type+'-'+(item.location||'')+'-'+(item.date||'')+'-'+((item.info||'').slice(0,30));
  const cardState=actionStates[reviewKey]||{};
  const actions=suggestActions(item, type, enabledActions);

  const handleAction=(action)=>{
    /* If already sent/replied, open the modal */
    if(cardState.status==='sent'||cardState.status==='replied'){
      setEmailModal({
        email: cardState.email,
        reply: cardState.reply||null,
        actionLog: cardState.log||[],
        item, type
      });
      return;
    }

    /* Start sending */
    const email=generateEmail(item, type, action.id);
    const now=new Date();
    const log=[
      {action:'Review flagged', time:fmt(new Date(now.getTime()-86400000*2))+' '+fmtTime(new Date(now.getTime()-86400000*2)), status:''},
      {action: action.id==='respond'?'Response email sent':'Action: '+action.label, time:fmt(now)+' '+fmtTime(now), status:''},
    ];

    setActionStates(s=>({...s,[reviewKey]:{status:'sending',email,log}}));

    /* Simulate sending delay */
    setTimeout(()=>{
      const hasReply=Math.random()>0.4;
      const reply=hasReply?simulateReply(email,type):null;
      if(hasReply){
        log.push({action:'Customer replied', time:reply.delay+' later', status:''});
      }
      setActionStates(s=>({...s,[reviewKey]:{
        status:hasReply?'replied':'sent',
        email, reply, log
      }}));
      setToast('✓ Email sent from '+getFeedbackEmail());
    },2000);
  };

  const statusLabel=cardState.status==='sending'?'Sending...':cardState.status==='sent'?'Email Sent':cardState.status==='replied'?'Reply Received':null;
  const statusClass=cardState.status||'';

  return(
    <div className={`review-card${flag==='urgent'?' flagged':''}`}>
      <div className="review-header">
        <div className="review-meta">
          <span className="badge badge-location">{item.location}</span>
          {item.source&&<span className="badge badge-source">{item.source}</span>}
          {item.type&&<span className="badge badge-type">{item.type}</span>}
          {flag==='urgent'&&<span className="badge badge-urgent">⚠ URGENT</span>}
          {flag==='important'&&<span className="badge badge-complaint">Important</span>}
          <span className={`badge ${type==='complaint'?'badge-complaint':'badge-compliment'}`}>{type==='complaint'?'Complaint':'Compliment'}</span>
        </div>
        <span className="review-date">{item.date}</span>
      </div>
      <div className={`review-text${expanded?'':' truncated'}`} onClick={()=>setExpanded(!expanded)}>{item.info||'No details available'}</div>
      {item.customer_name&&<div className="review-customer">👤 {item.customer_name}</div>}

      {/* Action area */}
      <div className="suggestion-area" style={{marginTop:12,padding:14,background:'var(--surface2)',border:'1px solid var(--border)',borderRadius:'var(--r-sm)'}}>
        {!cardState.status&&<>
          <div className="suggestion-label">💡 Suggested Action</div>
          <div className="suggestion-actions">
            {actions.map(a=><button key={a.id} className="btn-action" onClick={()=>handleAction(a)}>
              <span>{a.icon}</span> {a.label}
            </button>)}
          </div>
        </>}
        {cardState.status==='sending'&&<div className="flex items-center gap-2">
          <div className="spinner"/>
          <span className="text-sm" style={{color:'var(--amber)',fontWeight:600}}>Sending email...</span>
        </div>}
        {(cardState.status==='sent'||cardState.status==='replied')&&<div>
          <button className={`btn-action ${statusClass}`} onClick={()=>handleAction(actions[0])} style={{cursor:'pointer'}}>
            {cardState.status==='replied'?I.reply:I.check}
            <span>{statusLabel}</span>
            <span style={{fontSize:10,opacity:.7}}>· click to view</span>
          </button>
          {cardState.log&&<div className="text-xs text-muted mt-2" style={{display:'flex',flexWrap:'wrap',gap:8}}>
            {cardState.log.map((l,i)=><span key={i}>{l.action}</span>)}
          </div>}
        </div>}
      </div>
    </div>
  );
}

/* ═══ DASHBOARD ═══ */
function DashboardPage({complaints,compliments,onNavigate}){
  const [showCal,setShowCal]=useState(false);
  const [dateFrom,setDateFrom]=useState(()=>daysAgo(30));
  const [dateTo,setDateTo]=useState(()=>new Date());
  const [timePeriod,setTimePeriod]=useState('30d');
  const setTime=(key,from,to)=>{setTimePeriod(key);setDateFrom(from);setDateTo(to)};
  const fc=useMemo(()=>complaints.filter(c=>{const d=parseDate(c.date);return d&&d>=dateFrom&&d<=dateTo}),[complaints,dateFrom,dateTo]);
  const fk=useMemo(()=>compliments.filter(c=>{const d=parseDate(c.date);return d&&d>=dateFrom&&d<=dateTo}),[compliments,dateFrom,dateTo]);
  const urgent=fc.filter(c=>flagReview(c.info)==='urgent').length;
  const pct=fc.length+fk.length?Math.round(fk.length/(fc.length+fk.length)*100):0;

  /* Chart */
  const chartRef=useRef(null);const chartInst=useRef(null);
  useEffect(()=>{
    if(!chartRef.current)return;
    if(chartInst.current)chartInst.current.destroy();
    const days={};const cur=new Date(dateFrom);
    while(cur<=dateTo){const k=cur.toISOString().slice(0,10);days[k]={complaints:0,compliments:0};cur.setDate(cur.getDate()+1)}
    fc.forEach(c=>{const k=c.date;if(days[k])days[k].complaints++});
    fk.forEach(c=>{const k=c.date;if(days[k])days[k].compliments++});
    const labels=Object.keys(days).map(k=>new Date(k).toLocaleDateString('en-GB',{day:'numeric',month:'short'}));
    chartInst.current=new Chart(chartRef.current,{type:'line',data:{labels,datasets:[{label:'Complaints',data:Object.values(days).map(d=>d.complaints),borderColor:'#d4372c',backgroundColor:'rgba(212,55,44,.08)',fill:true,tension:.3,pointRadius:2},{label:'Compliments',data:Object.values(days).map(d=>d.compliments),borderColor:'#16a34a',backgroundColor:'rgba(22,163,74,.08)',fill:true,tension:.3,pointRadius:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{boxWidth:12,padding:16,font:{family:'DM Sans',size:11}}}},scales:{x:{grid:{display:false},ticks:{font:{family:'DM Sans',size:10},maxRotation:0,maxTicksLimit:7}},y:{beginAtZero:true,grid:{color:'#f0efed'},ticks:{font:{family:'DM Sans',size:10}}}}}});
    return()=>{if(chartInst.current)chartInst.current.destroy()};
  },[fc,fk,dateFrom,dateTo]);

  return(
    <div>
      <div className="page-header"><h2>Dashboard</h2><p>{fmt(dateFrom)} – {fmt(dateTo)}</p></div>
      <div className="time-bar">
        <button className={`time-chip ${timePeriod==='lastweek'?'active':''}`} onClick={()=>setTime('lastweek',lastWeekStart(),lastWeekEnd())}>Last Week</button>
        <button className={`time-chip ${timePeriod==='30d'?'active':''}`} onClick={()=>setTime('30d',daysAgo(30),new Date())}>Last 30 Days</button>
        <button className={`time-chip ${timePeriod==='month'?'active':''}`} onClick={()=>setTime('month',startOfMonth(),new Date())}>This Month</button>
        <button className={`time-chip ${timePeriod==='custom'?'active':''}`} onClick={()=>{setTimePeriod('custom');setShowCal(true)}} style={{display:'inline-flex',alignItems:'center',gap:6}}>{I.calendar} Custom</button>
      </div>
      {showCal&&<CalendarPicker onClose={()=>setShowCal(false)} onSelect={(s,e)=>{setDateFrom(s);setDateTo(new Date(e.getTime()+86399999));setTimePeriod('custom')}} initStart={dateFrom} initEnd={dateTo}/>}
      <div className="kpi-grid" style={{marginBottom:20}}>
        <div className="kpi"><div className="kpi-label">Complaints</div><div className="kpi-value">{fc.length}</div></div>
        <div className="kpi"><div className="kpi-label">Compliments</div><div className="kpi-value" style={{color:'var(--green)'}}>{fk.length}</div></div>
        <div className="kpi"><div className="kpi-label">Urgent</div><div className="kpi-value" style={{color:urgent>0?'var(--red)':'var(--text)'}}>{urgent}</div></div>
        <div className="kpi"><div className="kpi-label">Satisfaction</div><div className="kpi-value">{pct}%</div></div>
      </div>
      <div className="chart-wrap"><div className="chart-title">Feedback Trend</div><div style={{height:260}}><canvas ref={chartRef}/></div></div>
      <div className="card" style={{cursor:'pointer'}} onClick={()=>onNavigate('reviews')}>
        <div className="flex items-center justify-between">
          <div><div className="text-sm font-bold">Recent Reviews</div><div className="text-xs text-muted mt-2">{fc.length+fk.length} reviews in period</div></div>
          <span style={{fontSize:20}}>→</span>
        </div>
      </div>
    </div>
  );
}

/* ═══ REVIEWS PAGE ═══ */
function ReviewsPage({complaints,compliments,enabledActions,actionStates,setActionStates,setToast,setEmailModal}){
  const [showCal,setShowCal]=useState(false);
  const [dateFrom,setDateFrom]=useState(()=>daysAgo(30));
  const [dateTo,setDateTo]=useState(()=>new Date());
  const [timePeriod,setTimePeriod]=useState('30d');
  const [location,setLocation]=useState('');
  const [type,setType]=useState('');
  const [source,setSource]=useState('');
  const [search,setSearch]=useState('');
  const [feedType,setFeedType]=useState('all');
  const [flagOnly,setFlagOnly]=useState(false);
  const [page,setPage]=useState(1);
  const perPage=15;

  const all=useMemo(()=>{
    let items=[];
    if(feedType!=='compliments')items.push(...complaints.map(c=>({...c,_type:'complaint'})));
    if(feedType!=='complaints')items.push(...compliments.map(c=>({...c,_type:'compliment'})));
    return items.filter(c=>{
      const d=parseDate(c.date);if(!d||d<dateFrom||d>dateTo)return false;
      if(location&&c.location!==location)return false;
      if(type&&c.type!==type)return false;
      if(source&&c.source!==source)return false;
      if(search){const s=search.toLowerCase();if(!(c.info||'').toLowerCase().includes(s)&&!(c.customer_name||'').toLowerCase().includes(s))return false}
      if(flagOnly&&!flagReview(c.info))return false;
      return true;
    }).sort((a,b)=>{const da=parseDate(a.date),db=parseDate(b.date);return db-da});
  },[complaints,compliments,dateFrom,dateTo,location,type,source,search,feedType,flagOnly]);

  const types=[...new Set(complaints.map(c=>c.type).filter(Boolean))];
  const sources=[...new Set([...complaints,...compliments].map(c=>c.source).filter(Boolean))];
  const tp=Math.ceil(all.length/perPage);
  const paged=all.slice((page-1)*perPage,page*perPage);

  return(
    <div>
      <div className="page-header"><h2>Reviews</h2><p>{fmt(dateFrom)} – {fmt(dateTo)} · {all.length} results</p></div>
      <div className="time-bar">
        <button className={`time-chip ${timePeriod==='lastweek'?'active':''}`} onClick={()=>{setTimePeriod('lastweek');setDateFrom(lastWeekStart());setDateTo(lastWeekEnd())}}>Last Week</button>
        <button className={`time-chip ${timePeriod==='30d'?'active':''}`} onClick={()=>{setTimePeriod('30d');setDateFrom(daysAgo(30));setDateTo(new Date())}}>Last 30 Days</button>
        <button className={`time-chip ${timePeriod==='month'?'active':''}`} onClick={()=>{setTimePeriod('month');setDateFrom(startOfMonth());setDateTo(new Date())}}>This Month</button>
        <button className={`time-chip ${timePeriod==='custom'?'active':''}`} onClick={()=>{setTimePeriod('custom');setShowCal(true)}} style={{display:'inline-flex',alignItems:'center',gap:6}}>{I.calendar} Custom</button>
      </div>
      {showCal&&<CalendarPicker onClose={()=>setShowCal(false)} onSelect={(s,e)=>{setDateFrom(s);setDateTo(new Date(e.getTime()+86399999))}} initStart={dateFrom} initEnd={dateTo}/>}
      <div className="filter-bar">
        <div className="toggle-group">
          <button className={`toggle-btn ${feedType==='all'?'active':''}`} onClick={()=>{setFeedType('all');setPage(1)}}>All</button>
          <button className={`toggle-btn ${feedType==='complaints'?'active':''}`} onClick={()=>{setFeedType('complaints');setPage(1)}}>Complaints</button>
          <button className={`toggle-btn ${feedType==='compliments'?'active':''}`} onClick={()=>{setFeedType('compliments');setPage(1)}}>Compliments</button>
        </div>
        <select className="filter-select" value={location} onChange={e=>{setLocation(e.target.value);setPage(1)}}><option value="">All Locations</option>{LOCATIONS.map(l=><option key={l.id} value={l.name}>{l.name}</option>)}{[...new Set([...complaints,...compliments].map(c=>c.location))].filter(loc=>!LOCATIONS.find(l=>l.name===loc)).sort().map(loc=><option key={loc} value={loc}>{loc} (Closed)</option>)}</select>
        <select className="filter-select" value={source} onChange={e=>{setSource(e.target.value);setPage(1)}}><option value="">All Sources</option>{sources.sort().map(s=><option key={s} value={s}>{s}</option>)}</select>
        {feedType!=='compliments'&&<select className="filter-select" value={type} onChange={e=>{setType(e.target.value);setPage(1)}}><option value="">All Types</option>{types.map(t=><option key={t} value={t}>{t}</option>)}</select>}
        <input className="filter-input" placeholder="Search reviews..." value={search} onChange={e=>{setSearch(e.target.value);setPage(1)}}/>
        <button className={`time-chip ${flagOnly?'active':''}`} onClick={()=>{setFlagOnly(!flagOnly);setPage(1)}}>⚠ Flagged</button>
      </div>
      {paged.map((item,i)=><ReviewCard key={`${item._type}-${i}-${item.date}`} item={item} type={item._type} enabledActions={enabledActions} actionStates={actionStates} setActionStates={setActionStates} setToast={setToast} setEmailModal={setEmailModal}/>)}
      {all.length===0&&<div style={{textAlign:'center',padding:48,color:'var(--text3)'}}><p>No reviews match your filters</p></div>}
      {tp>1&&<div className="pagination"><button className="page-btn" disabled={page<=1} onClick={()=>setPage(page-1)}>←</button>{Array.from({length:Math.min(tp,7)},(_,i)=>{let p;if(tp<=7)p=i+1;else if(page<=4)p=i+1;else if(page>=tp-3)p=tp-6+i;else p=page-3+i;return<button key={p} className={`page-btn ${page===p?'active':''}`} onClick={()=>setPage(p)}>{p}</button>})}<button className="page-btn" disabled={page>=tp} onClick={()=>setPage(page+1)}>→</button></div>}
    </div>
  );
}

/* ═══ REPORT PAGE ═══ */
function ReportPage({complaints,compliments}){
  const [showCal,setShowCal]=useState(false);
  const [dateFrom,setDateFrom]=useState(()=>daysAgo(30));
  const [dateTo,setDateTo]=useState(()=>new Date());
  const [timePeriod,setTimePeriod]=useState('30d');
  const [location,setLocation]=useState('');
  const prevFrom=new Date(dateFrom.getTime()-(dateTo-dateFrom));const prevTo=new Date(dateFrom.getTime()-1);
  const fc=useMemo(()=>complaints.filter(c=>{const d=parseDate(c.date);return d&&d>=dateFrom&&d<=dateTo&&(!location||c.location===location)}),[complaints,dateFrom,dateTo,location]);
  const fk=useMemo(()=>compliments.filter(c=>{const d=parseDate(c.date);return d&&d>=dateFrom&&d<=dateTo&&(!location||c.location===location)}),[compliments,dateFrom,dateTo,location]);
  const prevC=useMemo(()=>complaints.filter(c=>{const d=parseDate(c.date);return d&&d>=prevFrom&&d<=prevTo&&(!location||c.location===location)}),[complaints,prevFrom,prevTo,location]);
  const prevK=useMemo(()=>compliments.filter(c=>{const d=parseDate(c.date);return d&&d>=prevFrom&&d<=prevTo&&(!location||c.location===location)}),[compliments,prevFrom,prevTo,location]);

  const locScores=LOCATIONS.filter(l=>!location||l.name===location).map(l=>{
    const comp=fc.filter(c=>c.location===l.name).length;
    const compl=fk.filter(c=>c.location===l.name).length;
    const total=comp+compl;
    const score=total?Math.round((compl/total)*100):0;
    const prevComp=prevC.filter(c=>c.location===l.name).length;
    const prevCompl=prevK.filter(c=>c.location===l.name).length;
    const prevTotal=prevComp+prevCompl;
    const prevScore=prevTotal?Math.round((prevCompl/prevTotal)*100):0;
    return {...l,complaints:comp,compliments:compl,score,prevScore,change:score-prevScore};
  }).sort((a,b)=>b.score-a.score);

  const typeCounts={};fc.forEach(c=>{if(c.type)typeCounts[c.type]=(typeCounts[c.type]||0)+1});
  const top3=Object.entries(typeCounts).sort((a,b)=>b[1]-a[1]).slice(0,3);
  const prevTypeCounts={};prevC.forEach(c=>{if(c.type)prevTypeCounts[c.type]=(prevTypeCounts[c.type]||0)+1});

  const suggestions=[
    top3[0]?{cat:top3[0][0],text:top3[0][0].includes('Missing')||top3[0][0].includes('Wrong')?'Implement double-check system before dispatch — have a second team member verify orders against receipts':top3[0][0].includes('Quality')?'Schedule weekly supplier quality reviews and add daily prep standards checklist':'Review staffing levels and implement customer service refresher training',prio:'High'}:null,
    top3[1]?{cat:top3[1][0],text:top3[1][0].includes('Service')?'Run monthly team coaching sessions focused on greeting, speed, and complaint resolution':'Create standardised preparation guides with photo references for consistency',prio:'Medium'}:null,
    top3[2]?{cat:top3[2][0],text:'Set up automated alerts when this category exceeds weekly average by 20%',prio:'Monitor'}:null,
  ].filter(Boolean);

  const maxScore=Math.max(...locScores.map(l=>l.score),1);
  return(
    <div>
      <div className="page-header"><div className="flex items-center gap-2"><h2>Report</h2><InfoIcon text="Scores = % positive feedback. Actions tracked via email system."/></div><p>Performance overview & improvement insights</p></div>
      <div className="time-bar">
        <button className={`time-chip ${timePeriod==='lastweek'?'active':''}`} onClick={()=>{setTimePeriod('lastweek');setDateFrom(lastWeekStart());setDateTo(lastWeekEnd())}}>Last Week</button>
        <button className={`time-chip ${timePeriod==='30d'?'active':''}`} onClick={()=>{setTimePeriod('30d');setDateFrom(daysAgo(30));setDateTo(new Date())}}>Last 30 Days</button>
        <button className={`time-chip ${timePeriod==='month'?'active':''}`} onClick={()=>{setTimePeriod('month');setDateFrom(startOfMonth());setDateTo(new Date())}}>This Month</button>
        <button className={`time-chip ${timePeriod==='lastmonth'?'active':''}`} onClick={()=>{setTimePeriod('lastmonth');setDateFrom(startOfLastMonth());setDateTo(endOfLastMonth())}}>Last Month</button>
        <button className={`time-chip ${timePeriod==='custom'?'active':''}`} onClick={()=>{setTimePeriod('custom');setShowCal(true)}} style={{display:'inline-flex',alignItems:'center',gap:6}}>{I.calendar} Custom</button>
      </div>
      <div style={{marginBottom:16}}><select className="filter-select" value={location} onChange={e=>setLocation(e.target.value)}><option value="">All Locations</option>{LOCATIONS.map(l=><option key={l.id} value={l.name}>{l.name}</option>)}</select></div>
      {showCal&&<CalendarPicker onClose={()=>setShowCal(false)} onSelect={(s,e)=>{setDateFrom(s);setDateTo(new Date(e.getTime()+86399999))}} initStart={dateFrom} initEnd={dateTo}/>}
      <div className="card" style={{marginBottom:16}}>
        <div className="chart-title">Improvement Scale — Previous vs Current Period</div>
        <div className="text-xs text-muted mb-3">Comparing {fmt(prevFrom)} – {fmt(prevTo)} → {fmt(dateFrom)} – {fmt(dateTo)}</div>
        <div style={{display:'grid',gap:12,gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))'}}>
          {[{label:'Total Complaints',cur:fc.length,prev:prevC.length,good:'down'},{label:'Total Compliments',cur:fk.length,prev:prevK.length,good:'up'},{label:'Urgent Issues',cur:fc.filter(c=>flagReview(c.info)==='urgent').length,prev:prevC.filter(c=>flagReview(c.info)==='urgent').length,good:'down'},{label:'Satisfaction',cur:fc.length+fk.length?Math.round(fk.length/(fc.length+fk.length)*100):0,prev:prevC.length+prevK.length?Math.round(prevK.length/(prevC.length+prevK.length)*100):0,good:'up',pct:true}].map(m=>{
            const diff=m.cur-m.prev;const isGood=(m.good==='up'&&diff>0)||(m.good==='down'&&diff<0);
            return <div key={m.label} style={{padding:14,background:'var(--surface2)',borderRadius:'var(--r-sm)',textAlign:'center'}}>
              <div className="text-xs font-bold text-muted" style={{marginBottom:6}}>{m.label}</div>
              <div style={{fontSize:22,fontWeight:800}}>{m.cur}{m.pct?'%':''}</div>
              <div className="text-xs" style={{color:isGood?'var(--green)':diff===0?'var(--text3)':'var(--red)',fontWeight:600,marginTop:4,display:'flex',alignItems:'center',justifyContent:'center',gap:4}}>
                {diff>0?'↑':'↓'}{Math.abs(diff)}{m.pct?'%':''} <span className="text-light">was {m.prev}{m.pct?'%':''}</span>
              </div>
            </div>
          })}
        </div>
      </div>
      <div className="card" style={{marginBottom:16}}>
        <div className="chart-title">Location Score — Best to Worst</div>
        <div className="text-xs text-muted mb-3">Score = % positive feedback out of total</div>
        {locScores.map((l,i)=><div key={l.id} className="rank-row">
          <div className={`rank-num ${i===0?'gold':i===1?'silver':i===2?'bronze':''}`}>{i+1}</div>
          <div style={{flex:'1 1 100px',minWidth:0}}>
            <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:4}}>
              <div style={{width:8,height:8,borderRadius:'50%',background:l.color,flexShrink:0}}/>
              <span className="text-sm font-bold">{l.name}</span>
              <span className="text-xs" style={{marginLeft:'auto',fontWeight:700,color:l.score>=70?'var(--green)':l.score>=50?'var(--amber)':'var(--red)'}}>{l.score}%</span>
            </div>
            <div style={{background:'var(--surface2)',borderRadius:4,height:8,overflow:'hidden'}}>
              <div className="rank-bar" style={{width:l.score/maxScore*100+'%',background:l.score>=70?'var(--green)':l.score>=50?'var(--amber)':'var(--red)'}}/>
            </div>
            <div className="text-xs mt-2" style={{display:'flex',gap:12,color:'var(--text3)'}}>
              <span>{l.complaints} complaints</span><span>{l.compliments} compliments</span>
              <span style={{color:l.change>0?'var(--green)':l.change<0?'var(--red)':'var(--text3)',fontWeight:600}}>{l.change>0?'↑':l.change<0?'↓':'='}{Math.abs(l.change)}% vs prev</span>
            </div>
          </div>
        </div>)}
      </div>
      <div className="card" style={{marginBottom:16}}>
        <div className="chart-title">Top 3 Complaint Categories</div>
        <div style={{display:'grid',gap:12,gridTemplateColumns:'repeat(auto-fit,minmax(200px,1fr))'}}>
          {top3.map(([cat,count],i)=>{
            const prevCount=prevTypeCounts[cat]||0;
            const change=prevCount?Math.round(((count-prevCount)/prevCount)*100):0;
            return <div key={cat} style={{padding:16,background:i===0?'var(--red-soft)':i===1?'var(--amber-soft)':'var(--surface2)',borderRadius:'var(--r-sm)',border:'1px solid var(--border)'}}>
              <div className="text-xs font-bold" style={{color:i===0?'var(--red)':i===1?'var(--amber)':'var(--text2)',marginBottom:4}}>#{i+1}</div>
              <div className="text-sm font-bold" style={{marginBottom:2}}>{cat}</div>
              <div style={{fontSize:24,fontWeight:800,letterSpacing:'-1px'}}>{count}</div>
              <div className="text-xs" style={{color:change>0?'var(--red)':change<0?'var(--green)':'var(--text3)',fontWeight:600,marginTop:4}}>{change>0?'↑':change<0?'↓':'='}{Math.abs(change)}% vs previous period</div>
            </div>
          })}
        </div>
      </div>
      <div className="card">
        <div className="chart-title">Suggested Actions for Improvement</div>
        {suggestions.map((s,i)=><div key={i} style={{padding:14,background:'var(--surface2)',borderRadius:'var(--r-sm)',marginBottom:10,borderLeft:'3px solid '+(s.prio==='High'?'var(--red)':s.prio==='Medium'?'var(--amber)':'var(--blue)')}}>
          <div className="flex items-center gap-2 mb-2">
            <span className="badge" style={{background:s.prio==='High'?'var(--red-soft)':s.prio==='Medium'?'var(--amber-soft)':'var(--blue-soft)',color:s.prio==='High'?'var(--red)':s.prio==='Medium'?'var(--amber)':'var(--blue)'}}>{s.prio}</span>
            <span className="text-xs font-bold text-muted">Re: {s.cat}</span>
          </div>
          <div className="text-sm">{s.text}</div>
        </div>)}
      </div>
    </div>
  );
}

/* ═══ PERFORMANCE PAGE (normalised by store age) ═══ */
function LocationsPage({complaints,compliments}){
  const fys=fyStart();const fye=fyEnd();const fyL=fyLabel();
  const fc=complaints.filter(c=>{const d=parseDate(c.date);return d&&d>=fys&&d<=fye});
  const fk=compliments.filter(c=>{const d=parseDate(c.date);return d&&d>=fys&&d<=fye});
  const locData=LOCATIONS.map(l=>{
    const comp=fc.filter(c=>c.location===l.name);
    const compl=fk.filter(c=>c.location===l.name);
    const total=comp.length+compl.length;
    const rawScore=total?Math.round(compl.length/total*100):0;
    const mo=monthsOpen(l.openedDate, fye);
    const compPerMonth=mo?(comp.length/mo).toFixed(1):0;
    const complPerMonth=mo?(compl.length/mo).toFixed(1):0;
    const typeCounts={};comp.forEach(c=>{if(c.type)typeCounts[c.type]=(typeCounts[c.type]||0)+1});
    const topType=Object.entries(typeCounts).sort((a,b)=>b[1]-a[1])[0];
    return {...l,complaints:comp.length,compliments:compl.length,score:rawScore,monthsOpen:mo,compPerMonth,complPerMonth,topComplaint:topType?topType[0]:'-',topCount:topType?topType[1]:0,urgent:comp.filter(c=>flagReview(c.info)==='urgent').length};
  }).sort((a,b)=>b.score-a.score);
  const best=locData[0];const worst=locData[locData.length-1];
  return(
    <div>
      <div className="page-header"><h2>Performance</h2><p>{fyL} · Financial year April – March · Normalised by months open</p></div>
      <div style={{display:'grid',gap:16,gridTemplateColumns:'repeat(auto-fit,minmax(260px,1fr))',marginBottom:24}}>
        <div className="card" style={{borderTop:'4px solid var(--green)'}}>
          <div className="text-xs font-bold" style={{color:'var(--green)',marginBottom:8}}>BEST PERFORMER</div>
          <div style={{fontSize:20,fontWeight:800,marginBottom:4}}>{best.name}</div>
          <div style={{fontSize:36,fontWeight:800,color:'var(--green)',letterSpacing:'-2px'}}>{best.score}%</div>
          <div className="text-xs text-muted mt-2">{best.compliments} compliments · {best.complaints} complaints · {best.monthsOpen} months open</div>
        </div>
        <div className="card" style={{borderTop:'4px solid var(--red)'}}>
          <div className="text-xs font-bold" style={{color:'var(--red)',marginBottom:8}}>NEEDS ATTENTION</div>
          <div style={{fontSize:20,fontWeight:800,marginBottom:4}}>{worst.name}</div>
          <div style={{fontSize:36,fontWeight:800,color:'var(--red)',letterSpacing:'-2px'}}>{worst.score}%</div>
          <div className="text-xs text-muted mt-2">{worst.compliments} compliments · {worst.complaints} complaints · {worst.monthsOpen} months open</div>
        </div>
      </div>
      <div className="card">
        <div className="chart-title">All Locations — {fyL}</div>
        <div className="text-xs text-muted mb-3">Scores adjusted for store maturity. Per-month rates shown for fair comparison.</div>
        {locData.map((l,i)=><div key={l.id} className="rank-row">
          <div className={`rank-num ${i===0?'gold':i===1?'silver':i===2?'bronze':''}`}>{i+1}</div>
          <div style={{flex:1,minWidth:0}}>
            <div className="flex items-center gap-2" style={{marginBottom:4}}>
              <div style={{width:8,height:8,borderRadius:'50%',background:l.color}}/><span className="text-sm font-bold">{l.name}</span>
              {l.monthsOpen<=12&&<span className="badge" style={{background:'var(--blue-soft)',color:'var(--blue)',fontSize:9}}>New · {l.monthsOpen}mo</span>}
              <span style={{marginLeft:'auto',fontWeight:800,color:l.score>=70?'var(--green)':l.score>=50?'var(--amber)':'var(--red)'}}>{l.score}%</span>
            </div>
            <div style={{background:'var(--surface2)',borderRadius:4,height:8,overflow:'hidden',marginBottom:6}}>
              <div className="rank-bar" style={{width:l.score+'%',background:l.score>=70?'var(--green)':l.score>=50?'var(--amber)':'var(--red)'}}/>
            </div>
            <div className="text-xs" style={{display:'flex',flexWrap:'wrap',gap:10,color:'var(--text3)'}}>
              <span style={{color:'var(--red)'}}>{l.complaints} complaints ({l.compPerMonth}/mo)</span>
              <span style={{color:'var(--green)'}}>{l.compliments} compliments ({l.complPerMonth}/mo)</span>
              {l.urgent>0&&<span style={{color:'var(--red)',fontWeight:700}}>⚠ {l.urgent} urgent</span>}
              <span>Top: {l.topComplaint} ({l.topCount})</span>
              <span className="text-light">Open since {new Date(l.openedDate).toLocaleDateString('en-GB',{month:'short',year:'numeric'})}</span>
            </div>
          </div>
        </div>)}
      </div>
    </div>
  );
}

/* ═══ MYSTERY SHOPPER ═══ */
function MysteryShopperPage({mysteryCats}){
  const cats=mysteryCats||DEFAULT_MYSTERY_CATS;
  const [scores,setScores]=useState({});const [location,setLocation]=useState('');const [comment,setComment]=useState('');const [toast,setToast]=useState('');
  const [currentCat,setCurrentCat]=useState(0);const [swipeX,setSwipeX]=useState(0);const touchStart=useRef(0);
  const [showQuestions,setShowQuestions]=useState(false);
  const total=cats.reduce((a,c)=>a+((scores[c.name]||0)/10)*c.w,0);const max=cats.reduce((a,c)=>a+c.w,0);const pct=max?(total/max*100):0;
  const handleTouchStart=(e)=>{touchStart.current=e.touches[0].clientX;setSwipeX(0)};
  const handleTouchMove=(e)=>{setSwipeX(e.touches[0].clientX-touchStart.current)};
  const handleTouchEnd=()=>{if(swipeX<-60&&currentCat<cats.length-1)setCurrentCat(currentCat+1);if(swipeX>60&&currentCat>0)setCurrentCat(currentCat-1);setSwipeX(0)};
  const cat=cats[currentCat];
  const cameraRef=useRef(null);const [photo,setPhoto]=useState(null);
  const takePhoto=()=>{if(cameraRef.current)cameraRef.current.click()};
  const handleFile=(e)=>{const file=e.target.files[0];if(file){const url=URL.createObjectURL(file);setPhoto(url);setToast('Photo attached!')}};
  return(<div>{toast&&<Toast msg={toast} onClose={()=>setToast('')}/>}<div className="page-header"><h2>Mystery Shopper</h2><p>Submit evaluations — swipe to score · {cats.length} categories</p></div>
    <div className="card" style={{marginBottom:16}}>
      <div style={{marginBottom:16}}><label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:6}}>Location</label><select className="filter-select" value={location} onChange={e=>setLocation(e.target.value)} style={{width:'100%',maxWidth:300}}><option value="">Select location...</option>{LOCATIONS.map(l=><option key={l.id} value={l.name}>{l.name}</option>)}</select></div>
      <div className="text-xs font-bold text-muted mb-2" style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
        <span>Swipe left/right to navigate · Category {currentCat+1}/{cats.length}</span>
        <button className="text-xs" style={{color:'var(--blue)',fontWeight:600,cursor:'pointer'}} onClick={()=>setShowQuestions(!showQuestions)}>{showQuestions?'Hide':'Show'} Questions</button>
      </div>
      <div className="swipe-area" onTouchStart={handleTouchStart} onTouchMove={handleTouchMove} onTouchEnd={handleTouchEnd} style={{background:'var(--surface2)',borderRadius:'var(--r)',padding:24,textAlign:'center',marginBottom:16,transform:'translateX('+swipeX*.3+'px)',transition:swipeX===0?'transform .2s':'none',userSelect:'none',minHeight:180,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center'}}>
        <div className="text-xs text-muted" style={{marginBottom:4}}>{cat.w}% weight</div>
        <div style={{fontSize:18,fontWeight:700,marginBottom:8}}>{cat.name}</div>
        {showQuestions&&cat.questions&&cat.questions.length>0&&<div style={{marginBottom:12,textAlign:'left',width:'100%',padding:'8px 12px',background:'var(--surface)',borderRadius:'var(--r-sm)',border:'1px solid var(--border)'}}>
          {cat.questions.map((q,qi)=><div key={qi} style={{fontSize:12,color:'var(--text2)',padding:'3px 0',display:'flex',gap:6}}><span style={{color:'var(--text3)'}}>•</span>{q}</div>)}
        </div>}
        <div style={{display:'flex',gap:6,justifyContent:'center',flexWrap:'wrap'}}>
          {[0,1,2,3,4,5,6,7,8,9,10].map(n=><button key={n} onClick={()=>setScores({...scores,[cat.name]:n})} style={{width:36,height:36,borderRadius:'50%',border:scores[cat.name]===n?'2px solid var(--red)':'1px solid var(--border)',background:scores[cat.name]===n?'var(--red)':'var(--surface)',color:scores[cat.name]===n?'#fff':'var(--text)',fontWeight:700,fontSize:14,transition:'var(--t)'}}>{n}</button>)}
        </div>
        <div className="flex items-center justify-between" style={{width:'100%',marginTop:16}}>
          <button className="btn btn-sm btn-secondary" onClick={()=>currentCat>0&&setCurrentCat(currentCat-1)} disabled={currentCat===0}>← Prev</button>
          <div style={{display:'flex',gap:4}}>{cats.map((_,i)=><div key={i} style={{width:8,height:8,borderRadius:'50%',background:i===currentCat?'var(--red)':scores[cats[i].name]!==undefined?'var(--green)':'var(--border)'}}/>)}</div>
          <button className="btn btn-sm btn-secondary" onClick={()=>currentCat<cats.length-1&&setCurrentCat(currentCat+1)} disabled={currentCat===cats.length-1}>Next →</button>
        </div>
      </div>
      <div style={{marginBottom:16,padding:16,background:pct>=80?'var(--green-soft)':pct>=60?'var(--amber-soft)':'var(--red-soft)',borderRadius:'var(--r-sm)'}}><div className="text-xs font-bold" style={{color:pct>=80?'var(--green)':pct>=60?'var(--amber)':'var(--red)'}}>Score: {pct.toFixed(0)}% — {pct>=80?'PASS':pct>=60?'MARGINAL':'FAIL'}</div></div>
      <div style={{marginBottom:16}}><label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:6}}>Comments</label><textarea style={{width:'100%',padding:12,border:'1px solid var(--border)',borderRadius:'var(--r-sm)',resize:'vertical',minHeight:80,fontFamily:'var(--font)',fontSize:13}} value={comment} onChange={e=>setComment(e.target.value)} placeholder="Observations..."/></div>
      <div style={{marginBottom:16,display:'flex',gap:10,flexWrap:'wrap'}}>
        <input ref={cameraRef} type="file" accept="image/*" capture="environment" style={{display:'none'}} onChange={handleFile}/>
        <button className="btn btn-secondary btn-sm" onClick={takePhoto} style={{display:'inline-flex',alignItems:'center',gap:6}}>{I.camera} Take Photo</button>
        <label className="btn btn-secondary btn-sm" style={{cursor:'pointer',display:'inline-flex',alignItems:'center',gap:6}}>{I.upload} Upload<input type="file" accept="image/*" style={{display:'none'}} onChange={handleFile}/></label>
        {photo&&<img src={photo} alt="receipt" style={{width:48,height:48,borderRadius:'var(--r-sm)',objectFit:'cover',border:'2px solid var(--green)'}}/>}
      </div>
      <button className="btn btn-primary" onClick={()=>{if(!location){setToast('Select a location first');return}setToast('Report submitted!');setScores({});setComment('');setLocation('');setPhoto(null);setCurrentCat(0)}}>Submit</button>
    </div></div>);
}

/* ═══ INTEGRATIONS ═══ */
function IntegrationsPage({onNavigate,onPasteExtract}){
  const cfg=getReviewConfig();
  const locs=cfg.locations||{};
  const session=loadSession();
  const hasServer=!!(session&&session.email);
  const [manualModal,setManualModal]=useState(null);
  const [manualText,setManualText]=useState('');
  const [manualLoc,setManualLoc]=useState(LOCATIONS[0]?.id||'');
  const [manualType,setManualType]=useState('complaint');
  const [manualSource,setManualSource]=useState('Email');
  const [toast,setToast]=useState('');
  const [browseLoc,setBrowseLoc]=useState(LOCATIONS[0]?.id||'');

  const getLastScan=(platformId)=>{
    try{const d=JSON.parse(localStorage.getItem('fhub_last_scan')||'{}');return d[platformId]||null}catch(e){return null}
  };
  const setLastScan=(platformId,date)=>{
    try{const d=JSON.parse(localStorage.getItem('fhub_last_scan')||'{}');d[platformId]=date;localStorage.setItem('fhub_last_scan',JSON.stringify(d))}catch(e){}
  };

  const platformStatus=(platformId)=>{
    const configuredLocs=LOCATIONS.filter(l=>(locs[l.id]||{})[platformId]);
    if(!hasServer) return {status:'disconnected',label:'Not Signed In',locCount:configuredLocs.length};
    if(configuredLocs.length===0) return {status:'disconnected',label:'Not Configured',locCount:0};
    return {status:'connected',label:configuredLocs.length+'/'+LOCATIONS.length+' locations',locCount:configuredLocs.length};
  };

  const handleManualSubmit=()=>{
    if(!manualText.trim())return;
    const loc=LOCATIONS.find(l=>l.id===manualLoc);
    const review={info:manualText.trim(),location:loc?loc.name:'Unknown',source:manualSource,date:new Date().toISOString().slice(0,10),customer_name:''};
    const imported=getImportedReviews();
    if(manualType==='complaint'){if(!imported.complaints)imported.complaints=[];imported.complaints.push(review)}
    else{if(!imported.compliments)imported.compliments=[];imported.compliments.push(review)}
    saveImportedReviews(imported);
    setManualText('');setManualModal(null);setToast('Review added!');
  };

  const ints=[
    {id:'google',name:'Google Reviews',icon:'G',color:'#4285f4',bg:'#e8f0fe',method:'auto',howTo:'Automatic — reviews are fetched server-side via Google Places API. Set up your Google Place ID in Settings → Review Sources.',public:true},
    {id:'trustpilot',name:'Trustpilot',icon:'T',color:'#00b67a',bg:'#e0f5ed',method:'auto',howTo:'Automatic — reviews are fetched server-side. Set up your Trustpilot business URL in Settings → Review Sources.',public:true},
    {id:'tripadvisor',name:'TripAdvisor',icon:'TA',color:'#34e0a1',bg:'#e3faf0',method:'auto',howTo:'Automatic — reviews are fetched server-side. Set up your TripAdvisor listing URL in Settings → Review Sources.',public:true},
    {id:'deliveroo',name:'Deliveroo',icon:'D',color:'#00ccbc',bg:'#e0faf6',method:'browse',howTo:'Deliveroo requires login to view reviews. Click "Open Reviews Page" to navigate to your Deliveroo store\'s reviews & refunds page, then click "Scan Reviews" to let the AI extract them.',public:false,
      getUrl:(locId)=>{const u=(locs[locId]||{}).deliveroo;return u||null}},
    {id:'justeat',name:'Just Eat',icon:'J',color:'#f36d00',bg:'#fef0e5',method:'auto',howTo:'Automatic — reviews are fetched server-side. Set up your Just Eat restaurant URL in Settings → Review Sources.',public:true},
    {id:'email',name:'Email / Website',icon:'@',color:'#8b5cf6',bg:'#f3effe',method:'browse',howTo:'For feedback received by email, phone, in-person, or your website — click "Open Inbox" to navigate to your feedback email, then click "Scan" to let the AI extract reviews from recent messages.',public:true},
  ];

  const imported=getImportedReviews();
  const totalImported=(imported.complaints?.length||0)+(imported.compliments?.length||0);

  return(<div>{toast&&<Toast msg={toast} onClose={()=>setToast('')}/>}
    <div className="page-header"><h2>Integrations</h2><p>How reviews get into Feedback Hub</p></div>

    <div className="card" style={{marginBottom:16,display:'flex',alignItems:'center',justifyContent:'space-between',flexWrap:'wrap',gap:12}}>
      <div>
        <div className="text-sm font-bold">Import Engine</div>
        <div className="text-xs text-muted">{hasServer?<span style={{color:'var(--green)'}}>● Server connected</span>:<span style={{color:'var(--red)'}}>○ Not signed in</span>} · {totalImported} reviews imported</div>
      </div>
      <button className="btn btn-sm btn-primary" onClick={()=>onNavigate&&onNavigate('settings')}>Configure in Settings</button>
    </div>

    {ints.map(i=>{
      const st=platformStatus(i.id);
      return <div key={i.id} className="int-card">
        <div className="int-icon" style={{background:i.bg,color:i.color,fontSize:i.icon.length>1?14:20,fontWeight:800}}>{i.icon}</div>
        <div className="int-body">
          <div className="int-name">{i.name} <span className="badge" style={{fontSize:9,padding:'1px 6px',marginLeft:6,background:i.method==='auto'?'var(--green-soft)':i.method==='browse'?'var(--amber-soft)':i.method==='paste'?'var(--amber-soft)':'var(--blue-soft)',color:i.method==='auto'?'var(--green)':i.method==='browse'?'var(--amber)':i.method==='paste'?'var(--amber)':'var(--blue)'}}>{i.method==='auto'?'Automatic':i.method==='browse'?'Scan & Import':i.method==='paste'?'Paste & Extract':'Manual Entry'}</span></div>
          <div className="int-desc" style={{marginBottom:6}}>{i.howTo}</div>
          <div className="flex items-center gap-2" style={{flexWrap:'wrap'}}>
            <span className={`int-status ${st.status==='connected'?'int-connected':'int-disconnected'}`}>
              {st.status==='connected'?'● '+st.label:'○ '+st.label}
            </span>
            {i.method==='paste'&&onPasteExtract&&<button className="btn btn-sm btn-secondary" style={{fontSize:11,padding:'4px 12px'}} onClick={()=>{
              if(st.locCount>0){const firstLoc=LOCATIONS.find(l=>(locs[l.id]||{})[i.id]);if(firstLoc)onPasteExtract({platform:i.name,locationId:firstLoc.id})}
              else{onPasteExtract({platform:i.name,locationId:LOCATIONS[0]?.id||''})}
            }}>📋 Open Paste & Extract</button>}
            {i.method==='manual'&&<button className="btn btn-sm btn-secondary" style={{fontSize:11,padding:'4px 12px'}} onClick={()=>setManualModal(true)}>✏️ Add Review Manually</button>}
            {i.method==='auto'&&st.status==='disconnected'&&<button className="btn btn-sm btn-secondary" style={{fontSize:11,padding:'4px 12px'}} onClick={()=>onNavigate&&onNavigate('settings')}>Set Up</button>}
            {i.method==='browse'&&(()=>{
              const lastScan=getLastScan(i.id);
              const btnLabel=i.id==='deliveroo'?'🔗 Open Reviews Page':i.id==='email'?'📧 Open Inbox':'🔗 Open';
              const scanLabel=i.id==='deliveroo'?'📥 Scan Reviews':i.id==='email'?'📥 Scan Inbox':'📥 Scan';
              return <React.Fragment>
                {i.id==='deliveroo'&&<React.Fragment>
                  <select className="filter-select" style={{fontSize:11,padding:'4px 8px',minWidth:120}} value={browseLoc} onChange={e=>setBrowseLoc(e.target.value)}>
                    {LOCATIONS.map(l=><option key={l.id} value={l.id}>{l.name}</option>)}
                  </select>
                  <button className="btn btn-sm btn-secondary" style={{fontSize:11,padding:'4px 12px'}} onClick={()=>{
                    const url=i.getUrl&&i.getUrl(browseLoc);
                    if(url){window.open(url,'_blank')}
                    else{setToast('No Deliveroo URL configured for this location. Set it in Settings → Review Sources.')}
                  }}>{btnLabel}</button>
                </React.Fragment>}
                {i.id==='email'&&<button className="btn btn-sm btn-secondary" style={{fontSize:11,padding:'4px 12px'}} onClick={()=>{
                  const emailUrl=cfg.emailInboxUrl||'https://mail.google.com';
                  window.open(emailUrl,'_blank');
                }}>{btnLabel}</button>}
                <button className="btn btn-sm btn-primary" style={{fontSize:11,padding:'4px 12px'}} onClick={()=>{
                  setToast('Scan feature coming soon — reviews were last extracted via AI assistant.');
                  setLastScan(i.id,new Date().toISOString());
                }}>{scanLabel}</button>
                {lastScan&&<span className="text-xs text-muted" style={{marginLeft:4}}>Last scan: {new Date(lastScan).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'})}</span>}
              </React.Fragment>;
            })()}
          </div>
        </div>
      </div>;
    })}

    {/* Manual review entry modal */}
    {manualModal&&<div style={{position:'fixed',inset:0,zIndex:999,display:'flex',alignItems:'center',justifyContent:'center',background:'rgba(0,0,0,.5)'}}>
      <div className="card" style={{width:480,maxWidth:'90vw',padding:24}}>
        <div className="flex items-center justify-between" style={{marginBottom:16}}>
          <h3 style={{fontSize:16,fontWeight:700}}>Add Review Manually</h3>
          <button style={{background:'none',border:'none',fontSize:18,cursor:'pointer',color:'var(--text3)'}} onClick={()=>setManualModal(null)}>✕</button>
        </div>
        <div style={{marginBottom:12}}>
          <label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:4}}>Location</label>
          <select className="filter-select" style={{width:'100%'}} value={manualLoc} onChange={e=>setManualLoc(e.target.value)}>
            {LOCATIONS.map(l=><option key={l.id} value={l.id}>{l.name}</option>)}
          </select>
        </div>
        <div style={{marginBottom:12}}>
          <label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:4}}>Type</label>
          <div className="toggle-group">
            <button className={`toggle-btn ${manualType==='complaint'?'active':''}`} onClick={()=>setManualType('complaint')}>Complaint</button>
            <button className={`toggle-btn ${manualType==='compliment'?'active':''}`} onClick={()=>setManualType('compliment')}>Compliment</button>
          </div>
        </div>
        <div style={{marginBottom:12}}>
          <label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:4}}>Source</label>
          <select className="filter-select" style={{width:'100%'}} value={manualSource} onChange={e=>setManualSource(e.target.value)}>
            {['Email','Website','Phone','In-Person','Social Media','Other'].map(s=><option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div style={{marginBottom:16}}>
          <label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:4}}>Review Text</label>
          <textarea style={{width:'100%',padding:10,border:'1px solid var(--border)',borderRadius:'var(--r-sm)',resize:'vertical',minHeight:100,fontFamily:'var(--font)',fontSize:13}} value={manualText} onChange={e=>setManualText(e.target.value)} placeholder="Paste or type the customer feedback here..."/>
        </div>
        <div className="flex gap-2">
          <button className="btn btn-primary" onClick={handleManualSubmit} disabled={!manualText.trim()}>Add Review</button>
          <button className="btn btn-secondary" onClick={()=>setManualModal(null)}>Cancel</button>
        </div>
      </div>
    </div>}
  </div>);
}

/* ═══ DIGEST ═══ */
function DigestPage(){
  const [freq,setFreq]=useState('weekly');const [day,setDay]=useState('monday');
  const [recip,setRecip]=useState(()=>{const a=getCurrentAccount();return a.adminEmails?a.adminEmails.join(', '):''});
  const [sections,setSections]=useState({summary:true,urgent:true,trends:true,locations:true,compliments:true,mystery:false});
  const [toast,setToast]=useState('');
  return(<div>{toast&&<Toast msg={toast} onClose={()=>setToast('')}/>}
    <div className="page-header"><div className="flex items-center gap-2"><h2>Email Digest</h2><InfoIcon text="Sends a scheduled feedback summary to your team."/></div><p>Automated summary to your inbox</p></div>
    <div className="digest-layout">
      <div className="digest-config"><div className="card">
        <h3 style={{fontSize:15,fontWeight:700,marginBottom:16}}>Configuration</h3>
        <div style={{marginBottom:16}}><label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:6}}>Frequency</label><div className="toggle-group">{['daily','weekly','monthly'].map(f=><button key={f} className={`toggle-btn ${freq===f?'active':''}`} onClick={()=>setFreq(f)}>{f.charAt(0).toUpperCase()+f.slice(1)}</button>)}</div></div>
        {freq==='weekly'&&<div style={{marginBottom:16}}><label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:6}}>Send On</label><select className="filter-select" value={day} onChange={e=>setDay(e.target.value)}>{['monday','tuesday','wednesday','thursday','friday','saturday','sunday'].map(d=><option key={d} value={d}>{d.charAt(0).toUpperCase()+d.slice(1)}</option>)}</select></div>}
        <div style={{marginBottom:16}}><label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:6}}>Recipients</label><textarea style={{width:'100%',padding:10,border:'1px solid var(--border)',borderRadius:'var(--r-sm)',resize:'vertical',minHeight:60,fontFamily:'var(--font)',fontSize:12}} value={recip} onChange={e=>setRecip(e.target.value)}/></div>
        <div style={{marginBottom:20}}><label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:12}}>Include in Digest</label>{Object.entries(sections).map(([k,v])=><div key={k} style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'8px 0',borderBottom:'1px solid var(--border)'}}><span className="text-sm" style={{textTransform:'capitalize'}}>{k.replace(/([A-Z])/g,' $1')}</span><div className={`switch ${v?'on':''}`} onClick={()=>setSections({...sections,[k]:!v})}/></div>)}</div>
        <div className="flex gap-2"><button className="btn btn-primary" onClick={()=>setToast('Settings saved!')}>Save</button><button className="btn btn-secondary" onClick={()=>setToast('Test email sent!')}>Send Test</button></div>
      </div></div>
      <div className="digest-preview"><div className="card"><div className="flex items-center justify-between mb-3"><h3 style={{fontSize:15,fontWeight:700}}>Preview</h3><span className="text-xs text-light">How the email looks</span></div>
        <div className="digest-preview-box">
          <div style={{textAlign:'center',marginBottom:20}}><div style={{marginBottom:8}}><FeedbackHubLogo size={48}/></div><div style={{fontSize:18,fontWeight:700}}>{getBusinessName()} — Weekly Digest</div><div className="text-xs text-light">From {getFeedbackEmail()}</div></div>
          {sections.summary&&<div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)',marginBottom:12}}><div className="text-xs font-bold" style={{color:'var(--red)',marginBottom:6}}>WEEKLY SUMMARY</div><div className="text-sm">42 complaints · 67 compliments · 3 urgent</div></div>}
          {sections.urgent&&<div style={{padding:16,background:'var(--red-soft)',borderRadius:'var(--r-sm)',marginBottom:12}}><div className="text-xs font-bold" style={{color:'var(--red)',marginBottom:6}}>⚠ URGENT</div><div className="text-sm">Food poisoning report — Camden<br/>Allergy incident — Soho</div></div>}
          {sections.trends&&<div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)',marginBottom:12}}><div className="text-xs font-bold mb-2" style={{color:'var(--blue)'}}>TRENDS</div><div className="text-sm">Missing items ↑18% · Service ↓12%</div></div>}
          {sections.locations&&<div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)',marginBottom:12}}><div className="text-xs font-bold mb-2" style={{color:'var(--green)'}}>LOCATIONS</div><div className="text-sm">Best: Swains Lane · Watch: Fulham</div></div>}
          {sections.compliments&&<div style={{padding:16,background:'var(--green-soft)',borderRadius:'var(--r-sm)',marginBottom:12}}><div className="text-xs font-bold mb-2" style={{color:'var(--green)'}}>TOP COMPLIMENTS</div><div className="text-sm">"Best bagels in London!" — Google, Soho</div></div>}
        </div>
      </div></div>
    </div></div>);
}

/* ═══ SETTINGS with configurable actions ═══ */
function SettingsPage({enabledActions, setEnabledActions, mysteryCats, setMysteryCats, users, setUsers, onImportComplete}){
  const {updateAccount}=useAccount()||{};
  const [toast,setToast]=useState('');
  const [newActionLabel,setNewActionLabel]=useState('');
  const [addingLocation,setAddingLocation]=useState(false);
  const [newLocName,setNewLocName]=useState('');
  const [newLocAddress,setNewLocAddress]=useState('');
  const [newLocColor,setNewLocColor]=useState('#d4372c');
  const LOC_COLORS=['#d4372c','#2563eb','#7c3aed','#16a34a','#d97706','#0891b2','#be185d','#6366f1','#ea580c','#059669'];
  const [newActionIcon,setNewActionIcon]=useState('📌');
  const [settingsTab,setSettingsTab]=useState('sources');
  const [reviewCfg,setReviewCfg]=useState(()=>getReviewConfig());
  const [importing,setImporting]=useState(false);
  const [importStatus,setImportStatus]=useState('');
  const [importResults,setImportResults]=useState(null);
  const [expandedLoc,setExpandedLoc]=useState(null);
  const [editingCat,setEditingCat]=useState(null);
  const [editingUser,setEditingUser]=useState(null);
  const [newUserName,setNewUserName]=useState('');
  const [newUserEmail,setNewUserEmail]=useState('');

  const toggleAction=(id)=>{
    setEnabledActions(prev=>prev.map(a=>a.id===id?{...a,disabled:!a.disabled}:a));
  };
  const removeAction=(id)=>{
    setEnabledActions(prev=>prev.filter(a=>a.id!==id));
    setToast('Action removed');
  };
  const addAction=()=>{
    if(!newActionLabel.trim())return;
    const id='custom_'+Date.now();
    setEnabledActions(prev=>[...prev,{id,label:newActionLabel.trim(),icon:newActionIcon,keywords:[],forType:null,removable:true}]);
    setNewActionLabel('');
    setToast('Action added');
  };

  /* Mystery category editing */
  const updateCatName=(catId,name)=>{setMysteryCats(prev=>prev.map(c=>c.id===catId?{...c,name}:c))};
  const updateCatWeight=(catId,w)=>{setMysteryCats(prev=>prev.map(c=>c.id===catId?{...c,w:Math.max(0,Math.min(100,parseInt(w)||0))}:c))};
  const addCatQuestion=(catId)=>{setMysteryCats(prev=>prev.map(c=>c.id===catId?{...c,questions:[...(c.questions||[]),'']}:c))};
  const updateCatQuestion=(catId,qi,val)=>{setMysteryCats(prev=>prev.map(c=>c.id===catId?{...c,questions:c.questions.map((q,i)=>i===qi?val:q)}:c))};
  const removeCatQuestion=(catId,qi)=>{setMysteryCats(prev=>prev.map(c=>c.id===catId?{...c,questions:c.questions.filter((_,i)=>i!==qi)}:c))};
  const addCategory=()=>{
    const id='cat_'+Date.now();
    setMysteryCats(prev=>[...prev,{id,name:'New Category',w:10,questions:['New question?']}]);
    setEditingCat(id);
    setToast('Category added');
  };
  const removeCategory=(catId)=>{setMysteryCats(prev=>prev.filter(c=>c.id!==catId));setToast('Category removed')};

  /* User permissions */
  const toggleUserPerm=(userId,perm)=>{setUsers(prev=>prev.map(u=>u.id===userId?{...u,permissions:{...u.permissions,[perm]:!u.permissions[perm]}}:u))};
  const setUserLocationAccess=(userId,val)=>{setUsers(prev=>prev.map(u=>u.id===userId?{...u,locationAccess:val}:u))};
  const toggleUserLocation=(userId,locId)=>{
    setUsers(prev=>prev.map(u=>{
      if(u.id!==userId)return u;
      if(u.locationAccess==='all')return{...u,locationAccess:LOCATIONS.map(l=>l.id).filter(id=>id!==locId)};
      const arr=Array.isArray(u.locationAccess)?u.locationAccess:[];
      return{...u,locationAccess:arr.includes(locId)?arr.filter(id=>id!==locId):[...arr,locId]};
    }));
  };
  const addUser=()=>{
    if(!newUserName.trim()||!newUserEmail.trim())return;
    const id='u_'+Date.now();
    setUsers(prev=>[...prev,{id,name:newUserName.trim(),email:newUserEmail.trim(),role:'Viewer',permissions:{dashboard:true,reviews:true,report:true,locations:true,mystery:false,integrations:false,digest:false,settings:false},locationAccess:'all'}]);
    setNewUserName('');setNewUserEmail('');setToast('User added');
  };
  const removeUser=(userId)=>{setUsers(prev=>prev.filter(u=>u.id!==userId));setToast('User removed')};
  const cycleRole=(userId)=>{
    const roles=['Admin','Manager','Viewer'];
    setUsers(prev=>prev.map(u=>{if(u.id!==userId)return u;const i=roles.indexOf(u.role);return{...u,role:roles[(i+1)%roles.length]}}));
  };

  const totalWeight=mysteryCats.reduce((a,c)=>a+c.w,0);

  const tabs=[{id:'sources',label:'Review Sources'},{id:'actions',label:'Actions'},{id:'mystery',label:'Mystery Shopper'},{id:'permissions',label:'Permissions'},{id:'locations',label:'Locations'},{id:'email',label:'Email'},{id:'data',label:'Data'}];

  return(<div>{toast&&<Toast msg={toast} onClose={()=>setToast('')}/>}<div className="page-header"><h2>Settings</h2><p>Configure your Feedback Hub</p></div>

    <div style={{display:'flex',gap:6,flexWrap:'wrap',marginBottom:20}}>
      {tabs.map(t=><button key={t.id} className={`time-chip ${settingsTab===t.id?'active':''}`} onClick={()=>setSettingsTab(t.id)}>{t.label}</button>)}
    </div>

    {/* ═══ REVIEW SOURCES TAB ═══ */}
    {settingsTab==='sources'&&<div>
      {/* Server-Side Review Fetching */}
      <div className="card" style={{marginBottom:16}}>
        <div style={{display:'flex',alignItems:'flex-start',gap:12,marginBottom:16}}>
          <div style={{width:40,height:40,borderRadius:'var(--r-sm)',background:'var(--green-soft)',display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0}}>
            <span style={{fontSize:18}}>☁️</span>
          </div>
          <div style={{flex:1}}>
            <h3 style={{fontSize:15,fontWeight:700,marginBottom:2}}>Server-Side Review Engine</h3>
            <div className="text-xs text-muted" style={{lineHeight:1.6}}>Reviews are fetched directly by the Feedback Hub server from Google, Trustpilot, and TripAdvisor. Just configure your platform URLs below and click "Import Now".</div>
          </div>
        </div>
        <div style={{marginBottom:12}}>
          <label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:4}}>Google Places API Key <span className="text-light">(optional — for richer Google Reviews data)</span></label>
          <input className="filter-input" value={reviewCfg.googleApiKey||''} onChange={e=>{const c={...reviewCfg,googleApiKey:e.target.value};setReviewCfg(c);saveReviewConfig(c)}} placeholder="AIza..." style={{maxWidth:'none',width:'100%'}}/>
          <details style={{background:'var(--blue-soft,#e8f0fe)',borderRadius:'var(--r-sm)',padding:10,marginTop:8}}>
            <summary className="text-xs font-bold" style={{cursor:'pointer',color:'var(--blue)'}}>📋 How to get a Google Places API Key</summary>
            <ol className="text-xs text-muted" style={{paddingLeft:18,marginTop:8,lineHeight:2.0}}>
              <li>Go to <a href="https://console.cloud.google.com/" target="_blank" rel="noopener" style={{color:'var(--blue)',textDecoration:'underline'}}>Google Cloud Console</a> and sign in with your Google account.</li>
              <li>Create a new project (or select an existing one) from the top-left project dropdown.</li>
              <li>Open the <strong>Navigation menu ☰ → APIs &amp; Services → Library</strong>.</li>
              <li>Search for <strong>"Places API (New)"</strong> and click <strong>Enable</strong>.</li>
              <li>Go to <strong>APIs &amp; Services → Credentials</strong> and click <strong>+ CREATE CREDENTIALS → API key</strong>.</li>
              <li>Copy the key (starts with <code style={{background:'var(--surface2)',padding:'1px 4px',borderRadius:3}}>AIza...</code>) and paste it above.</li>
              <li><em>Recommended:</em> Click <strong>Restrict key</strong> → under "API restrictions" select <strong>Places API (New)</strong> only, to keep it secure.</li>
            </ol>
            <div className="text-xs text-muted" style={{marginTop:6,padding:'6px 8px',background:'var(--surface2)',borderRadius:4,lineHeight:1.5}}>
              <strong>💡 Tip:</strong> Google gives you $200/month of free API credits — enough for ~10,000 place-detail lookups. You won't be charged unless you exceed that.
            </div>
          </details>
        </div>
        <details style={{background:'var(--surface2)',borderRadius:'var(--r-sm)',padding:12}}>
          <summary className="text-xs font-bold" style={{cursor:'pointer',color:'var(--blue)'}}>Supported platforms</summary>
          <ul className="text-xs text-muted" style={{paddingLeft:18,marginTop:8,lineHeight:2}}>
            <li><strong>Google Reviews</strong> — Uses Places API if key provided, otherwise scrapes public data</li>
            <li><strong>Trustpilot</strong> — Scrapes business page reviews (up to 30)</li>
            <li><strong>TripAdvisor</strong> — Scrapes listing page reviews</li>
            <li><strong>Email forwarding</strong> — Forward customer emails to the review inbox</li>
          </ul>
        </details>
      </div>

      {/* Import Now + Status */}
      <div className="card" style={{marginBottom:16,display:'flex',alignItems:'center',justifyContent:'space-between',flexWrap:'wrap',gap:12}}>
        <div>
          <h3 style={{fontSize:15,fontWeight:700,marginBottom:2}}>Import Reviews</h3>
          <div className="text-xs text-muted">{importing?importStatus:'Click to fetch new reviews from all configured sources'}</div>
          {(()=>{const cfg=getReviewConfig();const last=cfg.lastAutoImport;return last?<div className="text-xs text-light" style={{marginTop:4}}>Last import: {new Date(last).toLocaleString('en-GB')}</div>:null})()}
        </div>
        <div className="flex gap-2">
          <button className={'btn btn-primary'+(importing?' btn-disabled':'')} disabled={importing} onClick={async()=>{
            const session=loadSession();
            if(!session||!session.email){setToast('Please sign in first');return}

            setImporting(true);setImportStatus('Starting import...');setImportResults(null);
            try{
              const result=await runFullImport((msg)=>setImportStatus(msg));
              setImportResults(result);
              if(result.total>0){
                if(onImportComplete) onImportComplete();
                setToast('Imported '+result.total+' new reviews!');
              }else if(result.errors&&result.errors.length>0){
                setToast(result.errors.length+' error(s) during import — see details below');
              }else{
                setToast('No new reviews found');
              }
            }catch(e){setToast('Import failed: '+e.message);setImportResults({total:0,errors:[e.message],details:[]})}
            setImporting(false);setImportStatus('');
          }}>{importing?<span style={{display:'inline-block',width:14,height:14,border:'2px solid #fff',borderTopColor:'transparent',borderRadius:'50%',animation:'spin 1s linear infinite'}}/>:'🔄'} {importing?'Importing...':'Import Now'}</button>
          <button className="btn btn-secondary btn-sm" onClick={()=>{
            const data=getImportedReviews();
            const total=(data.complaints?.length||0)+(data.compliments?.length||0);
            setToast('Imported reviews in storage: '+total);
          }}>Status</button>
        </div>
      </div>
      {importResults&&<div className="card" style={{marginBottom:16,padding:12}}>
        <div className="flex items-center justify-between" style={{marginBottom:8}}>
          <h4 style={{fontSize:13,fontWeight:700}}>Import Results</h4>
          <button className="text-xs" style={{background:'none',border:'none',cursor:'pointer',color:'var(--muted)'}} onClick={()=>setImportResults(null)}>✕</button>
        </div>
        {importResults.total>0&&<div style={{fontSize:12,color:'var(--green)',marginBottom:6,fontWeight:600}}>✓ {importResults.total} new reviews imported</div>}
        {Object.keys(importResults.details||{}).length>0&&<div style={{marginBottom:6}}>
          {Object.entries(importResults.details).map(([key,val])=><div key={key} className="text-xs" style={{color:'var(--green)',marginBottom:2}}>✓ {key}: fetched {val.fetched}, added {val.added}</div>)}
        </div>}
        {importResults.errors.length>0&&<div>
          <div className="text-xs font-bold" style={{color:'var(--red)',marginBottom:4}}>{importResults.errors.length} error(s):</div>
          {importResults.errors.map((err,i)=><div key={i} className="text-xs" style={{color:'var(--red)',marginBottom:2,padding:'4px 8px',background:'var(--red-soft)',borderRadius:4}}>✕ {err}</div>)}
        </div>}
        {importResults.total===0&&importResults.errors.length===0&&<div className="text-xs text-muted">No new reviews found across any source.</div>}
      </div>}

      {/* Per-location platform config */}
      <div className="card" style={{marginBottom:16}}>
        <h3 style={{fontSize:15,fontWeight:700,marginBottom:4}}>Location Review Sources</h3>
        <div className="text-xs text-muted mb-3">Configure review platform URLs for each location. Only locations with URLs will be fetched.</div>

        {LOCATIONS.map(loc=>{
          const locCfg=(reviewCfg.locations||{})[loc.id]||{};
          const configuredCount=REVIEW_PLATFORMS.filter(p=>locCfg[p.id]).length;
          const isExpanded=expandedLoc===loc.id;

          return <div key={loc.id} style={{marginBottom:8,border:'1px solid var(--border)',borderRadius:'var(--r-sm)',overflow:'hidden'}}>
            <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'12px 16px',background:'var(--surface2)',cursor:'pointer'}} onClick={()=>setExpandedLoc(isExpanded?null:loc.id)}>
              <div className="flex items-center gap-3">
                <div style={{width:10,height:10,borderRadius:'50%',background:loc.color}}/>
                <div>
                  <div className="text-sm font-bold">{loc.name}</div>
                  <div className="text-xs text-light">{configuredCount} source{configuredCount!==1?'s':''} configured</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {configuredCount>0&&<span style={{fontSize:11,fontWeight:600,color:'var(--green)'}}>● Active</span>}
                <span style={{fontSize:16,transform:isExpanded?'rotate(180deg)':'',transition:'var(--t)'}}>▾</span>
              </div>
            </div>
            {isExpanded&&<div style={{padding:16,borderTop:'1px solid var(--border)'}}>
              {REVIEW_PLATFORMS.map(platform=><div key={platform.id} style={{marginBottom:14}}>
                <div className="flex items-center gap-2" style={{marginBottom:4}}>
                  <div style={{width:24,height:24,borderRadius:4,background:platform.bg,color:platform.color,display:'flex',alignItems:'center',justifyContent:'center',fontSize:platform.icon.length>1?9:12,fontWeight:800,flexShrink:0}}>{platform.icon}</div>
                  <label className="text-xs font-bold">{platform.fieldLabel}</label>
                  {!platform.public&&<span className="badge" style={{fontSize:9,padding:'1px 6px',background:'var(--amber-soft)',color:'var(--amber)'}}>Login Required</span>}
                </div>
                <input className="filter-input" value={locCfg[platform.id]||''} onChange={e=>{
                  const newCfg={...reviewCfg};
                  if(!newCfg.locations) newCfg.locations={};
                  if(!newCfg.locations[loc.id]) newCfg.locations[loc.id]={};
                  newCfg.locations[loc.id][platform.id]=e.target.value;
                  setReviewCfg(newCfg);
                  saveReviewConfig(newCfg);
                }} placeholder={platform.fieldPlaceholder} style={{width:'100%',maxWidth:'none'}}/>
                <div className="text-xs text-light" style={{marginTop:2}}>{platform.fieldHelp}</div>
              </div>)}
            </div>}
          </div>;
        })}
      </div>

      {/* Quick bulk actions */}
      <div className="card" style={{marginBottom:16}}>
        <h3 style={{fontSize:15,fontWeight:700,marginBottom:8}}>Quick Actions</h3>
        <div className="flex gap-2" style={{flexWrap:'wrap'}}>
          <button className="btn btn-sm btn-secondary" onClick={()=>{
            const data=getImportedReviews();
            const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
            const url=URL.createObjectURL(blob);
            const a=document.createElement('a');a.href=url;a.download='feedbackhub-imported-reviews.json';a.click();
            URL.revokeObjectURL(url);
            setToast('Exported imported reviews');
          }}>Export Imported Reviews</button>
          <button className="btn btn-sm" style={{color:'var(--red)',fontWeight:600}} onClick={()=>{
            if(confirm('Clear all imported reviews from local storage? This cannot be undone.')){
              localStorage.removeItem(getStorageKey('reviews'));
              if(onImportComplete) onImportComplete();
              setToast('Imported reviews cleared');
            }
          }}>Clear Imported Reviews</button>
        </div>
      </div>
    </div>}

    {/* ═══ ACTIONS TAB ═══ */}
    {settingsTab==='actions'&&<div className="card" style={{marginBottom:20}}>
      <h3 style={{fontSize:15,fontWeight:700,marginBottom:4}}>Response Actions</h3>
      <div className="text-xs text-muted mb-3">Configure which actions are available on review cards. All responses are sent from <strong>{getFeedbackEmail()}</strong>.</div>
      {enabledActions.map(a=><div key={a.id} style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'10px 0',borderBottom:'1px solid var(--border)'}}>
        <div className="flex items-center gap-2">
          <span style={{fontSize:16}}>{a.icon}</span>
          <div>
            <div className="text-sm font-bold">{a.label}</div>
            <div className="text-xs text-light">{a.always?'Always shown':'Shown when keywords match'}{a.forType?' · '+a.forType+'s only':''}</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className={`switch ${!a.disabled?'on':''}`} onClick={()=>a.id!=='respond'&&toggleAction(a.id)}/>
          {a.removable!==false&&<button className="text-xs" style={{color:'var(--red)',fontWeight:600}} onClick={()=>removeAction(a.id)}>Remove</button>}
        </div>
      </div>)}
      <div style={{marginTop:16,padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)'}}>
        <div className="text-xs font-bold text-muted mb-2">Add Custom Action</div>
        <div className="flex gap-2" style={{flexWrap:'wrap'}}>
          <select className="filter-select" value={newActionIcon} onChange={e=>setNewActionIcon(e.target.value)} style={{width:60}}>
            {['📌','📞','🔔','📊','🔧','💬','📝','🏷️'].map(e=><option key={e} value={e}>{e}</option>)}
          </select>
          <input className="filter-input" value={newActionLabel} onChange={e=>setNewActionLabel(e.target.value)} placeholder="Action name..." style={{maxWidth:200}}/>
          <button className="btn btn-sm btn-primary" onClick={addAction}>Add</button>
        </div>
      </div>
    </div>}

    {/* ═══ MYSTERY SHOPPER TAB ═══ */}
    {settingsTab==='mystery'&&<div className="card" style={{marginBottom:20}}>
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:16}}>
        <div><h3 style={{fontSize:15,fontWeight:700,marginBottom:2}}>Mystery Shopper Categories</h3>
        <div className="text-xs text-muted">Edit categories, weights and questions. Total weight: <strong style={{color:totalWeight===100?'var(--green)':'var(--red)'}}>{totalWeight}%</strong>{totalWeight!==100&&' (should be 100%)'}</div></div>
        <button className="btn btn-sm btn-primary" onClick={addCategory}>+ Category</button>
      </div>
      {mysteryCats.map((cat,ci)=><div key={cat.id} style={{marginBottom:12,border:'1px solid var(--border)',borderRadius:'var(--r-sm)',overflow:'hidden'}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'12px 16px',background:'var(--surface2)',cursor:'pointer'}} onClick={()=>setEditingCat(editingCat===cat.id?null:cat.id)}>
          <div className="flex items-center gap-3">
            <span style={{fontSize:13,fontWeight:700,color:'var(--text3)',minWidth:20}}>{ci+1}</span>
            <div><div className="text-sm font-bold">{cat.name}</div><div className="text-xs text-light">{cat.w}% weight · {(cat.questions||[]).length} questions</div></div>
          </div>
          <div className="flex items-center gap-2">
            <span style={{fontSize:16,transform:editingCat===cat.id?'rotate(180deg)':'',transition:'var(--t)'}}>▾</span>
          </div>
        </div>
        {editingCat===cat.id&&<div style={{padding:16,borderTop:'1px solid var(--border)'}}>
          <div style={{display:'flex',gap:12,marginBottom:16,flexWrap:'wrap'}}>
            <div style={{flex:1,minWidth:160}}>
              <label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:4}}>Category Name</label>
              <input className="filter-input" value={cat.name} onChange={e=>updateCatName(cat.id,e.target.value)} style={{width:'100%',maxWidth:'none'}}/>
            </div>
            <div style={{width:80}}>
              <label className="text-xs font-bold text-muted" style={{display:'block',marginBottom:4}}>Weight %</label>
              <input className="score-input" type="number" min="0" max="100" value={cat.w} onChange={e=>updateCatWeight(cat.id,e.target.value)} style={{width:'100%'}}/>
            </div>
          </div>
          <div className="text-xs font-bold text-muted mb-2">Questions</div>
          {(cat.questions||[]).map((q,qi)=><div key={qi} style={{display:'flex',gap:8,marginBottom:6,alignItems:'center'}}>
            <span className="text-xs text-light" style={{minWidth:16}}>{qi+1}.</span>
            <input className="filter-input" value={q} onChange={e=>updateCatQuestion(cat.id,qi,e.target.value)} style={{flex:1,maxWidth:'none'}}/>
            <button style={{color:'var(--red)',fontWeight:700,fontSize:16,padding:'0 4px'}} onClick={()=>removeCatQuestion(cat.id,qi)}>×</button>
          </div>)}
          <div style={{display:'flex',gap:8,marginTop:8}}>
            <button className="btn btn-sm btn-secondary" onClick={()=>addCatQuestion(cat.id)}>+ Add Question</button>
            {mysteryCats.length>1&&<button className="btn btn-sm" style={{color:'var(--red)',fontWeight:600}} onClick={()=>{removeCategory(cat.id);setEditingCat(null)}}>Remove Category</button>}
          </div>
        </div>}
      </div>)}
    </div>}

    {/* ═══ PERMISSIONS TAB ═══ */}
    {settingsTab==='permissions'&&<div className="card" style={{marginBottom:20}}>
      <h3 style={{fontSize:15,fontWeight:700,marginBottom:4}}>Team & Permissions</h3>
      <div className="text-xs text-muted mb-3">Manage user access per feature and per location</div>
      {users.map(u=><div key={u.id} style={{marginBottom:16,border:'1px solid var(--border)',borderRadius:'var(--r-sm)',overflow:'hidden'}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'12px 16px',background:'var(--surface2)',cursor:'pointer'}} onClick={()=>setEditingUser(editingUser===u.id?null:u.id)}>
          <div><div className="text-sm font-bold">{u.name}</div><div className="text-xs text-light">{u.email}</div></div>
          <div className="flex items-center gap-2">
            <button className="badge badge-type" onClick={e=>{e.stopPropagation();cycleRole(u.id)}}>{u.role}</button>
            <span style={{fontSize:16,transform:editingUser===u.id?'rotate(180deg)':'',transition:'var(--t)'}}>▾</span>
          </div>
        </div>
        {editingUser===u.id&&<div style={{padding:16,borderTop:'1px solid var(--border)'}}>
          <div className="text-xs font-bold text-muted mb-2">Feature Access</div>
          <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(150px,1fr))',gap:8,marginBottom:16}}>
            {FEATURE_LIST.map(f=><label key={f.id} style={{display:'flex',alignItems:'center',gap:8,padding:'8px 12px',background:'var(--surface2)',borderRadius:'var(--r-sm)',cursor:'pointer',border:'1px solid '+(u.permissions[f.id]?'var(--green)':'var(--border)'),transition:'var(--t)'}}>
              <input type="checkbox" checked={!!u.permissions[f.id]} onChange={()=>toggleUserPerm(u.id,f.id)} style={{accentColor:'var(--green)',width:16,height:16}}/>
              <span className="text-xs font-bold" style={{color:u.permissions[f.id]?'var(--text)':'var(--text3)'}}>{f.label}</span>
            </label>)}
          </div>
          <div className="text-xs font-bold text-muted mb-2">Location Access</div>
          <div style={{marginBottom:8}}>
            <label style={{display:'flex',alignItems:'center',gap:8,padding:'8px 12px',background:'var(--surface2)',borderRadius:'var(--r-sm)',cursor:'pointer',marginBottom:8,border:'1px solid '+(u.locationAccess==='all'?'var(--green)':'var(--border)')}}>
              <input type="checkbox" checked={u.locationAccess==='all'} onChange={()=>setUserLocationAccess(u.id,u.locationAccess==='all'?LOCATIONS.map(l=>l.id):'all')} style={{accentColor:'var(--green)',width:16,height:16}}/>
              <span className="text-xs font-bold">All Locations</span>
            </label>
          </div>
          {u.locationAccess!=='all'&&<div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(130px,1fr))',gap:8}}>
            {LOCATIONS.map(l=>{const arr=Array.isArray(u.locationAccess)?u.locationAccess:[];const checked=arr.includes(l.id);return<label key={l.id} style={{display:'flex',alignItems:'center',gap:8,padding:'8px 12px',background:'var(--surface2)',borderRadius:'var(--r-sm)',cursor:'pointer',border:'1px solid '+(checked?l.color:'var(--border)')}}>
              <input type="checkbox" checked={checked} onChange={()=>toggleUserLocation(u.id,l.id)} style={{accentColor:l.color,width:16,height:16}}/>
              <div style={{width:8,height:8,borderRadius:'50%',background:l.color}}/>
              <span className="text-xs font-bold" style={{color:checked?'var(--text)':'var(--text3)'}}>{l.name}</span>
            </label>})}
          </div>}
          <div style={{marginTop:12,display:'flex',justifyContent:'flex-end'}}>
            <button className="btn btn-sm" style={{color:'var(--red)',fontWeight:600}} onClick={()=>removeUser(u.id)}>Remove User</button>
          </div>
        </div>}
      </div>)}
      <div style={{marginTop:16,padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)'}}>
        <div className="text-xs font-bold text-muted mb-2">Add Team Member</div>
        <div className="flex gap-2" style={{flexWrap:'wrap'}}>
          <input className="filter-input" value={newUserName} onChange={e=>setNewUserName(e.target.value)} placeholder="Name" style={{maxWidth:140}}/>
          <input className="filter-input" value={newUserEmail} onChange={e=>setNewUserEmail(e.target.value)} placeholder="email@company.com" style={{maxWidth:220}}/>
          <button className="btn btn-sm btn-primary" onClick={addUser}>Add</button>
        </div>
      </div>
    </div>}

    {/* ═══ LOCATIONS TAB ═══ */}
    {settingsTab==='locations'&&<div className="card" style={{marginBottom:20}}><h3 style={{fontSize:15,fontWeight:700,marginBottom:12}}>Locations</h3><div className="text-xs text-muted mb-3">Manage your stores and branches</div>
      {LOCATIONS.length===0&&!addingLocation&&<div style={{padding:24,textAlign:'center',background:'var(--surface2)',borderRadius:'var(--r-sm)',marginBottom:12}}><div style={{fontSize:28,marginBottom:8}}>📍</div><div className="text-sm font-bold mb-1">No locations yet</div><div className="text-xs text-muted mb-3">Add your first store or branch to start tracking feedback by location.</div><button className="btn btn-primary btn-sm" onClick={()=>setAddingLocation(true)}>+ Add Your First Location</button></div>}
      {LOCATIONS.map(l=><div key={l.id} style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'10px 0',borderBottom:'1px solid var(--border)'}}><div className="flex items-center gap-3"><div style={{width:10,height:10,borderRadius:'50%',background:l.color}}/><div><div className="text-sm font-bold">{l.name}</div><div className="text-xs text-light">{l.address}{l.openedDate&&(' · Open since '+new Date(l.openedDate).toLocaleDateString('en-GB',{month:'short',year:'numeric'}))}</div></div></div>
        <button className="btn btn-secondary btn-sm" style={{fontSize:11,padding:'4px 10px',color:'#b91c1c'}} onClick={()=>{if(confirm('Remove '+l.name+'?')){const newLocs=LOCATIONS.filter(x=>x.id!==l.id);if(updateAccount)updateAccount({locations:newLocs});setToast(l.name+' removed')}}}>Remove</button>
      </div>)}
      {addingLocation&&<div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)',marginTop:12,border:'2px solid var(--green)'}}>
        <div className="text-sm font-bold mb-2">Add New Location</div>
        <div style={{marginBottom:8}}><label className="text-xs text-muted" style={{display:'block',marginBottom:4}}>Name *</label><input className="filter-select" style={{width:'100%',maxWidth:300}} placeholder="e.g. Fulham, Main Street..." value={newLocName} onChange={e=>setNewLocName(e.target.value)}/></div>
        <div style={{marginBottom:8}}><label className="text-xs text-muted" style={{display:'block',marginBottom:4}}>Address</label><input className="filter-select" style={{width:'100%',maxWidth:400}} placeholder="e.g. 236 Fulham Rd, SW10 9NB" value={newLocAddress} onChange={e=>setNewLocAddress(e.target.value)}/></div>
        <div style={{marginBottom:12}}><label className="text-xs text-muted" style={{display:'block',marginBottom:4}}>Color</label><div className="flex items-center gap-2">{LOC_COLORS.map(c=><div key={c} onClick={()=>setNewLocColor(c)} style={{width:24,height:24,borderRadius:'50%',background:c,cursor:'pointer',border:newLocColor===c?'3px solid var(--text)':'3px solid transparent'}}/>)}</div></div>
        <div className="flex items-center gap-2">
          <button className="btn btn-primary btn-sm" onClick={()=>{if(!newLocName.trim()){setToast('Name is required');return}const id=newLocName.trim().toLowerCase().replace(/[^a-z0-9]+/g,'_');const newLoc={id,name:newLocName.trim(),address:newLocAddress.trim(),color:newLocColor,openedDate:new Date().toISOString().slice(0,10)};const newLocs=[...LOCATIONS,newLoc];if(updateAccount)updateAccount({locations:newLocs});setNewLocName('');setNewLocAddress('');setAddingLocation(false);setToast(newLocName.trim()+' added!')}}>Save Location</button>
          <button className="btn btn-secondary btn-sm" onClick={()=>{setAddingLocation(false);setNewLocName('');setNewLocAddress('')}}>Cancel</button>
        </div>
      </div>}
      {LOCATIONS.length>0&&!addingLocation&&<button className="btn btn-secondary btn-sm mt-3" onClick={()=>setAddingLocation(true)}>+ Add Location</button>}
    </div>}

    {/* ═══ EMAIL TAB ═══ */}
    {settingsTab==='email'&&<div className="card" style={{marginBottom:20}}><h3 style={{fontSize:15,fontWeight:700,marginBottom:12}}>Email</h3>
      <div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)'}}>
        <div className="flex items-center gap-3 mb-3"><span style={{fontSize:20}}>✉</span><div><div className="text-sm font-bold">{getFeedbackEmail()}</div><div className="text-xs text-muted">All customer responses are sent and received via this address</div></div></div>
        <div className="text-xs text-light">Replies from customers automatically appear on the review card. The action log tracks every email sent and response received.</div>
      </div>
    </div>}

    {/* ═══ DATA TAB ═══ */}
    {settingsTab==='data'&&<div className="card" style={{marginBottom:20}}><h3 style={{fontSize:15,fontWeight:700,marginBottom:12}}>Data</h3><div className="grid-2" style={{marginTop:12}}><div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)'}}><div className="text-sm font-bold mb-2">Export</div><div className="text-xs text-muted mb-3">Download as Excel/CSV</div><button className="btn btn-secondary btn-sm" onClick={()=>setToast('Export started')}>Export</button></div><div style={{padding:16,background:'var(--surface2)',borderRadius:'var(--r-sm)'}}><div className="text-sm font-bold mb-2">Transactions</div><div className="text-xs text-muted mb-3">Access & Fourth POS</div><button className="btn btn-secondary btn-sm">{I.upload} Upload</button></div></div></div>}

  </div>);
}

/* ═══ APP ═══ */
function App(){
  const acct=useAccount();
  const [page,setPage]=useState('dashboard');
  const [toast,setToast]=useState('');
  const [emailModal,setEmailModal]=useState(null);
  const [actionStates,setActionStates]=useState({});
  const [enabledActions,setEnabledActions]=useState(DEFAULT_ACTIONS.map(a=>({...a})));
  const [mysteryCats,setMysteryCats]=useState(DEFAULT_MYSTERY_CATS.map(c=>({...c,questions:[...(c.questions||[])]})));
  const [users,setUsers]=useState(()=>getDefaultUsers(acct));
  const [importedData,setImportedData]=useState(()=>getImportedReviews());
  const [pasteModal,setPasteModal]=useState(null);

  /* Set LOCATIONS dynamically from account */
  useEffect(()=>{
    if(acct&&acct.locations&&acct.locations.length>0){LOCATIONS=acct.locations}
    else if(acct&&acct.hasEmbeddedData){LOCATIONS=BBAGEL_LOCATIONS}
    else{LOCATIONS=[]}
  },[acct]);

  /* Merge embedded + imported reviews — only show embedded data for B Bagel account */
  const embeddedComplaints=(acct&&acct.hasEmbeddedData&&typeof COMPLAINT_DATA!=='undefined')?COMPLAINT_DATA:[];
  const embeddedCompliments=(acct&&acct.hasEmbeddedData&&typeof COMPLIMENT_DATA!=='undefined')?COMPLIMENT_DATA:[];
  const complaints=useMemo(()=>[...embeddedComplaints,...(importedData.complaints||[])],[embeddedComplaints,importedData]);
  const compliments=useMemo(()=>[...embeddedCompliments,...(importedData.compliments||[])],[embeddedCompliments,importedData]);

  /* Auto-import on first load (once per session) */
  const hasAutoImported=useRef(false);
  useEffect(()=>{
    if(hasAutoImported.current) return;
    hasAutoImported.current=true;
    const cfg=getReviewConfig();
    const sess=loadSession(); if(!sess||!sess.email) return;
    /* Check if last auto-import was less than 1 hour ago */
    const lastAuto=cfg.lastAutoImport||0;
    if(Date.now()-lastAuto<3600000) return;
    runFullImport().then(result=>{
      if(result.total>0){
        cfg.lastAutoImport=Date.now();
        saveReviewConfig(cfg);
        setImportedData(getImportedReviews());
        setToast('Auto-imported '+result.total+' new reviews');
      }
    }).catch(()=>{});
  },[]);
  const urgentCount=complaints.filter(c=>flagReview(c.info)==='urgent').length;
  const activeActions=enabledActions.filter(a=>!a.disabled);

  const renderPage=()=>{
    switch(page){
      case 'dashboard':return <DashboardPage complaints={complaints} compliments={compliments} onNavigate={setPage}/>;
      case 'reviews':return <ReviewsPage complaints={complaints} compliments={compliments} enabledActions={activeActions} actionStates={actionStates} setActionStates={setActionStates} setToast={setToast} setEmailModal={setEmailModal}/>;
      case 'report':return <ReportPage complaints={complaints} compliments={compliments}/>;
      case 'locations':return <LocationsPage complaints={complaints} compliments={compliments}/>;
      case 'mystery':return <MysteryShopperPage mysteryCats={mysteryCats}/>;
      case 'integrations':return <IntegrationsPage onNavigate={setPage} onPasteExtract={setPasteModal}/>;
      case 'digest':return <DigestPage/>;
      case 'settings':return <SettingsPage enabledActions={enabledActions} setEnabledActions={setEnabledActions} mysteryCats={mysteryCats} setMysteryCats={setMysteryCats} users={users} setUsers={setUsers} onImportComplete={()=>setImportedData(getImportedReviews())}/>;
      default:return <DashboardPage complaints={complaints} compliments={compliments} onNavigate={setPage}/>;
    }
  };
  const handlePasteExtracted=(reviews)=>{
    const imported=getImportedReviews();
    const apiQueue=[];
    reviews.forEach(r=>{
      const item={date:r.date,location:pasteModal.locationId,source:r.source,info:r.text,customer_name:r.author,rating:r.rating};
      const isCompliment=r.rating&&r.rating>=4||!r.rating;
      if(isCompliment){imported.compliments.push(item)}else{imported.complaints.push(item)}
      apiQueue.push({platform:r.source||pasteModal.platform,author:r.author||'Anonymous',rating:r.rating||null,text:r.text||'',date:r.date,location:pasteModal.locationId,type:isCompliment?'compliment':'complaint'});
    });
    saveImportedReviews(imported);
    setImportedData({...imported});
    setToast('Imported '+reviews.length+' reviews from '+pasteModal.platform);
    /* API sync */
    if(apiQueue.length>0){apiFetch('/api/reviews/bulk',{method:'POST',body:JSON.stringify({reviews:apiQueue})}).catch(()=>{})}
  };

  return(<div className="app">
    {toast&&<Toast msg={toast} onClose={()=>setToast('')}/>}
    {emailModal&&<EmailModal emailData={emailModal} onClose={()=>setEmailModal(null)}/>}
    {pasteModal&&<PasteExtractModal platform={pasteModal.platform} locationId={pasteModal.locationId} onExtracted={handlePasteExtracted} onClose={()=>setPasteModal(null)}/>}
    <aside className="sidebar"><div className="sidebar-logo"><FeedbackHubLogo size={42}/><div className="logo-text"><h1>{getBusinessName()}</h1><span>Feedback Hub</span></div></div><nav className="sidebar-nav"><div className="nav-section">Main</div>{NAV.slice(0,4).map(n=><button key={n.id} className={`nav-item ${page===n.id?'active':''}`} onClick={()=>setPage(n.id)}>{n.icon}<span>{n.label}</span></button>)}<div className="nav-section">Tools</div>{NAV.slice(4,7).map(n=><button key={n.id} className={`nav-item ${page===n.id?'active':''}`} onClick={()=>setPage(n.id)}>{n.icon}<span>{n.label}</span></button>)}<div className="nav-section">System</div>{NAV.slice(7).map(n=><button key={n.id} className={`nav-item ${page===n.id?'active':''}`} onClick={()=>setPage(n.id)}>{n.icon}<span>{n.label}</span></button>)}{acct&&acct.logout&&<button className="nav-item" onClick={acct.logout} style={{marginTop:16,color:'var(--text3)',fontSize:12}}><span style={{fontSize:14}}>↩</span><span>Sign Out</span></button>}</nav></aside>
    <main className="main">{renderPage()}</main>
    <nav className="bottom-nav">{[{id:'dashboard',icon:I.dashboard,l:'Home'},{id:'reviews',icon:I.feed,l:'Reviews'},{id:'report',icon:I.report,l:'Report'},{id:'locations',icon:I.trophy,l:'Perform.'},{id:'mystery',icon:I.mystery,l:'Shopper'},{id:'settings',icon:I.settings,l:'More'}].map(n=><button key={n.id} className={`nav-item ${page===n.id?'active':''}`} onClick={()=>setPage(n.id)}>{n.icon}<span>{n.l}</span></button>)}</nav>
  </div>);
}
/* ═══ ROOT: Login gate + Account provider ═══ */
function Root(){
  const [loggedIn,setLoggedIn]=useState(()=>!!loadSession());
  const [acct,setAcct]=useState(()=>{const s=loadSession();if(!s)return null;const accts=loadAccounts();return accts.find(a=>a.id===s.accountId)||null});

  const handleLogin=()=>{
    const s=loadSession();if(!s)return;
    const accts=loadAccounts();
    const a=accts.find(ac=>ac.id===s.accountId);
    if(a){LOCATIONS=a.locations&&a.locations.length?a.locations:(a.hasEmbeddedData?BBAGEL_LOCATIONS:[])}
    setAcct(a);
    setLoggedIn(true);
  };
  const handleLogout=()=>{clearSession();setLoggedIn(false);setAcct(null)};
  const updateAccount=(updates)=>{
    const accts=loadAccounts();
    const idx=accts.findIndex(a=>a.id===acct.id);
    if(idx===-1)return;
    const updated={...accts[idx],...updates};
    accts[idx]=updated;
    saveAccounts(accts);
    setAcct(updated);
    if(updated.locations&&updated.locations.length>0){LOCATIONS=updated.locations}
    else if(updated.hasEmbeddedData){LOCATIONS=BBAGEL_LOCATIONS}
    else{LOCATIONS=[]}
    /* Sync to API */
    const apiUp={};
    if(updates.businessName!==undefined)apiUp.name=updates.businessName;
    if(updates.locations!==undefined)apiUp.locations=updates.locations;
    if(updates.adminEmails!==undefined)apiUp.adminEmails=updates.adminEmails;
    if(Object.keys(apiUp).length>0)apiFetch('/api/account',{method:'PATCH',body:JSON.stringify(apiUp)}).catch(()=>{});
  };

  if(!loggedIn)return React.createElement(LoginScreen,{onLogin:handleLogin});
  return React.createElement(AccountCtx.Provider,{value:{...acct,logout:handleLogout,updateAccount}},
    React.createElement(App,null)
  );
}
ReactDOM.render(<Root/>,document.getElementById('root'));
</script>
</body>
</html>'''

output_path = 'index.html'
with open(output_path, 'w') as f:
    f.write(html)

size = os.path.getsize(output_path)
print(f"Written: {output_path}")
print(f"Size: {size:,} bytes")
print(f"Complaints: {len(complaints)}")
print(f"Compliments: {len(compliments)}")
