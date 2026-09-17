pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'

                bat 'if exist build rmdir /s /q build'
                bat 'mkdir build'

                bat 'copy app.py build\\app.py'
                bat 'copy prediction.py build\\prediction.py'
                bat 'copy housing_price_model_final.pkl build\\housing_price_model_final.pkl'
                bat 'copy requirements.txt build\\requirements.txt'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'build/**', fingerprint: true
                }
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

        stage('Deploy') {
            steps {
                bat 'if exist staging rmdir /s /q staging'
                bat 'mkdir staging'

                bat 'xcopy build staging /E /I /Y'

                bat 'echo Deploying verified application to staging environment'
                bat 'echo Staging deployment completed successfully'
            }
        }

        stage('Release') {
            steps {
                bat 'if exist production rmdir /s /q production'
                bat 'mkdir production'

                bat 'xcopy staging production /E /I /Y'

                bat 'if exist release.zip del /f /q release.zip'
                bat 'powershell -Command "Compress-Archive -Path production\\* -DestinationPath release.zip"'

                archiveArtifacts artifacts: 'release.zip', fingerprint: true

                bat 'echo Production release completed successfully'
            }
        }

        stage('Monitoring') {
            steps {
                bat 'echo Starting production application monitoring'
                bat 'echo Checking production application health'
                bat 'python -c "import urllib.request; response=urllib.request.urlopen(chr(104)+chr(116)+chr(116)+chr(112)+chr(58)+chr(47)+chr(47)+chr(108)+chr(111)+chr(99)+chr(97)+chr(108)+chr(104)+chr(111)+chr(115)+chr(116)+chr(58)+chr(56)+chr(53)+chr(48)+chr(49), timeout=10); print(response.status)"'
                bat 'echo Production application health check passed'
                bat 'echo Monitoring status: HEALTHY'
                bat 'echo Build number: %BUILD_NUMBER%'
                bat 'echo Job name: %JOB_NAME%'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully: Build -> Test -> Code Quality -> Security -> Deploy -> Release -> Monitoring'
        }

        failure {
            echo 'Pipeline failed. Review the failed stage and console output.'
        }
    }
}
