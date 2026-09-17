pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo '=== BUILD STAGE ==='

                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'

                bat 'if exist build rmdir /s /q build'
                bat 'mkdir build'

                bat 'copy app.py build\\app.py'
                bat 'copy prediction.py build\\prediction.py'
                bat 'copy housing_price_model_final.pkl build\\housing_price_model_final.pkl'
                bat 'copy requirements.txt build\\requirements.txt'

                echo 'Build artefact created successfully.'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'build/**', fingerprint: true
                }
            }
        }

        stage('Test') {
            steps {
                echo '=== TEST STAGE ==='

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
                echo '=== CODE QUALITY STAGE ==='

                bat 'python -m flake8 app.py prediction.py tests --max-line-length=120'

                echo 'Code quality checks passed.'
            }
        }

        stage('Security') {
            steps {
                echo '=== SECURITY STAGE ==='

                bat 'python -m pip_audit -r requirements.txt'

                echo 'Security audit passed. No known vulnerabilities found.'
            }
        }

        stage('Deploy') {
            steps {
                echo '=== DEPLOY STAGE ==='
                echo 'Deploying verified build to staging environment.'

                bat 'if exist staging rmdir /s /q staging'
                bat 'mkdir staging'

                bat 'xcopy build staging /E /I /Y'

                echo 'Starting Streamlit staging application on port 8502.'

                bat 'start "Streamlit-Staging" /B cmd /c "python -m streamlit run staging\\app.py --server.port 8502 --server.address 127.0.0.1 --server.headless true > staging.log 2>&1"'

                echo 'Waiting for staging application to start.'

                bat 'powershell -NoProfile -Command "$ok=$false; for($i=0;$i -lt 12;$i++){ try{$r=Invoke-WebRequest -Uri ''http://127.0.0.1:8502'' -UseBasicParsing -TimeoutSec 3; if($r.StatusCode -eq 200){$ok=$true; break}} catch{}; Start-Sleep -Seconds 2 }; if(-not $ok){Write-Host ''STAGING DEPLOYMENT FAILED''; exit 1}; Write-Host ''STAGING DEPLOYMENT SUCCESSFUL''"'
            }
        }

        stage('Release') {
            steps {
                echo '=== RELEASE STAGE ==='
                echo 'Promoting verified staging application to production.'

                bat 'if exist production rmdir /s /q production'
                bat 'mkdir production'

                bat 'xcopy staging production /E /I /Y'

                echo 'Stopping any previous production application.'

                bat 'for /f "tokens=5" %%a in (''netstat -ano ^| findstr :8501 ^| findstr LISTENING'') do taskkill /PID %%a /F'

                echo 'Starting production Streamlit application on port 8501.'

                bat 'start "Streamlit-Production" /B cmd /c "python -m streamlit run production\\app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true > production.log 2>&1"'

                echo 'Waiting for production application to start.'

                bat 'powershell -NoProfile -Command "$ok=$false; for($i=0;$i -lt 12;$i++){ try{$r=Invoke-WebRequest -Uri ''http://127.0.0.1:8501'' -UseBasicParsing -TimeoutSec 3; if($r.StatusCode -eq 200){$ok=$true; break}} catch{}; Start-Sleep -Seconds 2 }; if(-not $ok){Write-Host ''PRODUCTION RELEASE FAILED''; exit 1}; Write-Host ''PRODUCTION RELEASE SUCCESSFUL''"'

                bat 'if exist release.zip del /f /q release.zip'
                bat 'powershell -Command "Compress-Archive -Path production\\* -DestinationPath release.zip"'

                archiveArtifacts artifacts: 'release.zip', fingerprint: true
            }
        }

        stage('Monitoring') {
            steps {
                echo '=== MONITORING STAGE ==='
                echo 'Monitoring production application health.'

                bat 'powershell -NoProfile -Command "$ok=$false; try{$r=Invoke-WebRequest -Uri ''http://127.0.0.1:8501'' -UseBasicParsing -TimeoutSec 10; if($r.StatusCode -eq 200){$ok=$true}} catch{}; if($ok){Write-Host ''MONITORING: HEALTHY - Production application is responding.''} else {Write-Host ''ALERT: Production application is NOT responding.''; exit 1}"'

                bat 'echo Monitoring status: HEALTHY'
                bat 'echo Production endpoint: http://127.0.0.1:8501'
                bat 'echo Build number: %BUILD_NUMBER%'
                bat 'echo Job name: %JOB_NAME%'
            }
        }
    }

    post {
        success {
            echo '=== PIPELINE SUCCESS ==='
            echo 'Build -> Test -> Code Quality -> Security -> Deploy -> Release -> Monitoring'
            echo 'All pipeline stages completed successfully.'
        }

        failure {
            echo '=== PIPELINE ALERT ==='
            echo 'Pipeline failed. Check the failed stage and console output.'
            echo 'An unsuccessful health check or pipeline stage will stop the delivery process.'
        }
    }
}
