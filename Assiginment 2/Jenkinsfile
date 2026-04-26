pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'aceest-fitness'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_REPO = 'yourdockerhubusername/aceest-fitness'
        SONARQUBE_URL = 'http://localhost:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling source code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                echo 'Running Pytest unit tests...'
                sh '''
                    . venv/bin/activate
                    pytest test_app.py -v --tb=short --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube static code analysis...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=aceest-fitness \
                            -Dsonar.sources=. \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.host.url=${SONARQUBE_URL}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Checking SonarQube Quality Gate...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_REPO}:${DOCKER_TAG}"
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_REPO}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_REPO}:${DOCKER_TAG}
                        docker push ${DOCKER_REPO}:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes cluster...'
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/aceest-fitness -n aceest --timeout=120s
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'Running smoke tests against deployed application...'
                sh '''
                    sleep 10
                    HEALTH=$(kubectl exec -n aceest deploy/aceest-fitness -- curl -s http://localhost:5000/api/health)
                    echo "Health Check Response: $HEALTH"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! Application deployed.'
        }
        failure {
            echo 'Pipeline failed. Rolling back...'
            sh 'kubectl rollout undo deployment/aceest-fitness -n aceest || true'
        }
        always {
            cleanWs()
        }
    }
}
