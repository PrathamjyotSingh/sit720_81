pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pytest --junitxml=test-results.xml'
            }

            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
    }
}