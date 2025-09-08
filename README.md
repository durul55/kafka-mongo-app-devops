# Kafka-Mongo DevOps Project 🚀

Bu proje, **Flask tabanlı bir web servisi** üzerinden gelen HTTP isteklerini:
- Kafka’ya publish eder  
- Consumer ile consume edip MongoDB’ye kaydeder  
- Kubernetes üzerinde çalışır  
- CI/CD pipeline (GitHub Actions + ArgoCD) ile build & deploy olur  
- Prometheus & Grafana ile izlenir  

---

## 📂 Proje Yapısı;;

```
kafka-mongo-app-devops/
├── main.py                # Flask app
├── requirements.txt       # Python bağımlılıkları
├── Dockerfile             # Docker image build
├── helm/                  # Helm chart
│   ├── values.yaml
│   └── templates/
│       └── deployment.yaml
├── manifests/             # ArgoCD manifests
│   ├── application.yaml
│   └── namespace.yaml
├── .github/workflows/ci.yml  # GitHub Actions pipeline
└── README.md
```

---

## ⚙️ Kurulum

### 1. Docker Image Build & Push
```bash
docker build -t <registry>/kafka-mongo-app:latest .
docker push <registry>/kafka-mongo-app:latest
```

### 2. Helm ile Deploy
```bash
helm upgrade --install kafka-mongo-app ./helm -n dev
```

> Service dosyası yok. Uygulamayı erişilebilir yapmak için:
> - `kubectl port-forward` kullan  
> - veya ayrıca Service manifest ekle  

### 3. ArgoCD ile Continuous Delivery
```bash
kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/application.yaml
```

---

## 🌐 Uygulama Kullanımı;

Port-forward ile erişim:
```bash
kubectl port-forward deploy/kafka-mongo-app 5000:5000 -n dev
```

POST isteği gönder:
```bash
curl -X POST http://localhost:5000/publish   -H "Content-Type: application/json"   -d '{"value":"merhaba"}'
```

Cevap:
```json
{"message":"Value \"merhaba\" sent to Kafka"}
```

MongoDB’de doğrulama:
```bash
kubectl exec -it <mongo-pod> -n dev -- mongosh
use mydatabase
db.mycollection.find().pretty()
```

---

## 🔄 CI/CD Pipeline

- **GitHub Actions** ile her push’ta:
  - Docker image build & push
  - Versiyonlama (commit hash ile tag)
- **ArgoCD** otomatik olarak imajı çekip Kubernetes’e deploy eder

---

## 📊 Monitoring

Prometheus & Grafana kullanılır (kube-prometheus-stack).  

- CPU Kullanımı:
  ```promql
  sum(rate(container_cpu_usage_seconds_total{namespace="dev"}[1m])) by (pod)
  ```

- Memory Kullanımı:
  ```promql
  sum(container_memory_usage_bytes{namespace="dev"}) by (pod)
  ```

Grafana’da Dashboard import ederek grafiksel olarak görüntüleyebilirsin.

---

## 🛠️ Teknolojiler

- **Python Flask** – Web servisi  
- **Kafka** – Messaging  
- **MongoDB** – Data storage  
- **Docker** – Containerization  
- **Kubernetes + Helm** – Orchestration  
- **ArgoCD** – GitOps CD  
- **Prometheus + Grafana** – Monitoring  

---

## 📜 Lisans

MIT License
