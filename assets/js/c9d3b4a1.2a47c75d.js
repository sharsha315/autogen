"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9202],{16956:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>c,default:()=>d,frontMatter:()=>r,metadata:()=>o,toc:()=>i});var s=n(85893),a=n(11151);const r={sidebar_label:"utils",title:"agentchat.utils"},c=void 0,o={id:"reference/agentchat/utils",title:"agentchat.utils",description:"gather\\usage\\summary",source:"@site/docs/reference/agentchat/utils.md",sourceDirName:"reference/agentchat",slug:"/reference/agentchat/utils",permalink:"/autogen/docs/reference/agentchat/utils",draft:!1,unlisted:!1,editUrl:"https://github.com/microsoft/autogen/edit/main/website/docs/reference/agentchat/utils.md",tags:[],version:"current",frontMatter:{sidebar_label:"utils",title:"agentchat.utils"},sidebar:"referenceSideBar",previous:{title:"user_proxy_agent",permalink:"/autogen/docs/reference/agentchat/user_proxy_agent"},next:{title:"abstract_cache_base",permalink:"/autogen/docs/reference/cache/abstract_cache_base"}},l={},i=[{value:"gather_usage_summary",id:"gather_usage_summary",level:3}];function u(e){const t={code:"code",h3:"h3",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,a.a)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(t.h3,{id:"gather_usage_summary",children:"gather_usage_summary"}),"\n",(0,s.jsx)(t.pre,{children:(0,s.jsx)(t.code,{className:"language-python",children:"def gather_usage_summary(\n        agents: List[Agent]) -> Tuple[Dict[str, any], Dict[str, any]]\n"})}),"\n",(0,s.jsx)(t.p,{children:"Gather usage summary from all agents."}),"\n",(0,s.jsxs)(t.p,{children:[(0,s.jsx)(t.strong,{children:"Arguments"}),":"]}),"\n",(0,s.jsxs)(t.ul,{children:["\n",(0,s.jsxs)(t.li,{children:[(0,s.jsx)(t.code,{children:"agents"})," - (list): List of agents."]}),"\n"]}),"\n",(0,s.jsxs)(t.p,{children:[(0,s.jsx)(t.strong,{children:"Returns"}),":"]}),"\n",(0,s.jsxs)(t.ul,{children:["\n",(0,s.jsxs)(t.li,{children:[(0,s.jsx)(t.code,{children:"tuple"})," - (total_usage_summary, actual_usage_summary)"]}),"\n"]}),"\n",(0,s.jsxs)(t.p,{children:[(0,s.jsx)(t.strong,{children:"Example"}),":"]}),"\n",(0,s.jsx)(t.pre,{children:(0,s.jsx)(t.code,{className:"language-python",children:'total_usage_summary = {\n    "total_cost": 0.0006090000000000001,\n    "gpt-35-turbo": {\n            "cost": 0.0006090000000000001,\n            "prompt_tokens": 242,\n            "completion_tokens": 123,\n            "total_tokens": 365\n    }\n}\n'})}),"\n",(0,s.jsxs)(t.p,{children:[(0,s.jsx)(t.strong,{children:"Notes"}),":"]}),"\n",(0,s.jsxs)(t.p,{children:[(0,s.jsx)(t.code,{children:"actual_usage_summary"})," follows the same format.\nIf none of the agents incurred any cost (not having a client), then the total_usage_summary and actual_usage_summary will be ",(0,s.jsx)(t.code,{children:"{'total_cost': 0}"}),"."]})]})}function d(e={}){const{wrapper:t}={...(0,a.a)(),...e.components};return t?(0,s.jsx)(t,{...e,children:(0,s.jsx)(u,{...e})}):u(e)}},11151:(e,t,n)=>{n.d(t,{Z:()=>o,a:()=>c});var s=n(67294);const a={},r=s.createContext(a);function c(e){const t=s.useContext(r);return s.useMemo((function(){return"function"==typeof e?e(t):{...t,...e}}),[t,e])}function o(e){let t;return t=e.disableParentContext?"function"==typeof e.components?e.components(a):e.components||a:c(e.components),s.createElement(r.Provider,{value:t},e.children)}}}]);