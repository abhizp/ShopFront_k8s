FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

#docker and essentials for shell
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    gnupg \
    jq \
    unzip \
    ca-certificates \
    apt-transport-https \
    lsb-release \
    docker.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#gcloud
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl -https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update && apt-get install -y --no-install-recommends \
    google-cloud-cli \
    google-cloud-cli-gke-gcloud-auth-plugin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


#terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    terraform \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#python and ansible
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    ansible-core \
    google-auth \
    requests \
    pyyaml

#kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

#Install Helm
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
    chmod +0700 get_helm.sh && \
    ./get_helm.sh && \
    rm -f get_helm.sh

#verify
RUN echo "--- Verifying Toolchain ---" && \
    python3 --version && \
    ansible --version | head -n 1 && \
    gcloud --version | head -n 1 && \
    terraform -version | head -n 1 && \
    docker --version && \
    kubectl version --client && \
    helm version --short

WORKDIR /workspace

ENTRYPOINT ["/bin/bash"]