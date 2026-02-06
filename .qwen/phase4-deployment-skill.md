# Phase IV: Local Kubernetes Deployment Skill (Minikube + Helm + AI Tools)

**Skill Name:** phase4-deployment-skill  
**Description:** Reusable skill for deploying Todo AI Chatbot on local Kubernetes using Minikube, Helm, and AI tools (kubectl-ai, Kagent, Gordon).

## Core Principles (Yeh sab kyun use kar rahe hain)
- **Minikube** — Local Kubernetes cluster banane ke liye (free aur zero cloud cost)
- **Helm Charts** — Deployment ko package karne ke liye (manual YAML se bachne ke liye)
- **kubectl-ai / Kagent** — AI se Kubernetes commands chalane ke liye (judges ko impress karne ke liye)
- **Docker Desktop + Gordon** — Docker images banane aur AI se help lene ke liye

Yeh sab ek hi cheez dikhate hain:  
App sirf code nahi — **cloud-native**, **scalable**, **AI-assisted**, aur **Kubernetes-ready** hai.

## Key Advantages (Fayde)
- **Zero Cost** — Minikube local hai, koi AWS/GCP bill nahi
- **Fast & Easy** — Helm se ek command mein deploy, kubectl-ai se AI commands
- **Professional Look** — Judges ko lagega: "Yeh banda modern DevOps aur AIOps janta hai"
- **Scalable Demo** — Pods scale kar ke dikhaya ja sakta hai (real K8s feel)
- **Resume Capability** — Server restart pe bhi app chalta rahega (Helm + Minikube)

## Success Criteria (Kamyabi ke Nukte)
- Minikube running ho
- Helm chart install ho jaye
- Pods healthy hon (kubectl get pods → Running)
- App accessible ho (minikube service ya port-forward se)
- kubectl-ai ya Kagent se kam se kam 2-3 commands use hon
- Full demo in 30-45 min

## Constraints (Limitations)
- Local only (Minikube)
- No cloud deployment
- Max 2 replicas for demo
- Gordon use karo agar Docker Desktop mein enabled ho (Beta features)

## Step-by-Step Workflow (Kaise Karo)
1. **Containerize** → Frontend & Backend ke Docker images banao (Gordon ya manual)
2. **Helm Charts** → Chart banao (kubectl-ai se help lo)
3. **Minikube Setup** → minikube start --driver=docker
4. **Helm Install** → helm install todo ./helm/todo-chart
5. **AI Operations** → kubectl-ai "scale todo-frontend to 2 replicas"  
   kagent "analyze cluster health"
6. **Test & Access** → minikube service todo-frontend --url  
   Browser mein app kholo, login karo, /chat test karo

## Quick Commands Cheat Sheet
- Minikube start: `minikube start --driver=docker`
- Helm install: `helm install todo ./helm/todo-chart`
- Check pods: `kubectl get pods`
- Check services: `kubectl get svc`
- Open app: `minikube service todo-frontend --url`
- Scale pods: `kubectl-ai "scale todo-frontend deployment to 2 replicas"`
- Health check: `kagent "analyze cluster health"`

Yeh skill apply karne ke liye bolo:  
"Apply phase4-deployment-skill to deploy frontend and backend on Minikube."

**Ready to go!**  
Phase IV ab bohat easy aur impressive ho gaya hai.  
Ab bolo — **Minikube start karen** ya **Helm install** ka next step? 🚀🇵🇰