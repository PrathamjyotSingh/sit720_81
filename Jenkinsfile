pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                bat 'python --version'
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

        stage('Code Quality') {
            steps {
                bat 'python -m flake8 app.py prediction.py tests --max-line-length=120'
            }
        }

        stage('Security') {
            steps {
                bat 'python -m pip_audit -r requirements.txt'
            }
        }

        stage('Deployment') {
            steps {
                bat 'if exist deployment rmdir /s /q deployment'
                bat 'mkdir deployment'
                bat 'copy app.py deployment\\app.py'
                bat 'copy prediction.py deployment\\prediction.py'
                bat 'copy housing_price_model_final.pkl deployment\\housing_price_model_final.pkl'
                bat 'copy requirements.txt deployment\\requirements.txt'
            }
        }

        stage('Release') {
            steps {
                bat 'if exist release.zip del /f /q release.zip'
                bat 'powershell -Command "Compress-Archive -Path deployment\\* -DestinationPath release.zip"'
                archiveArtifacts artifacts: 'release.zip', fingerprint: true
            }
        }

        stage('Monitoring') {
            steps {
                bat 'echo Jenkins build monitoring completed successfully'
                bat 'echo Build number: %BUILD_NUMBER%'
                bat 'echo Job name: %JOB_NAME%'
                bat 'echo Build result: %BUILD_ID%'
            }
        }
    }
}