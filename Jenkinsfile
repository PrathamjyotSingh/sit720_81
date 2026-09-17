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

                archiveArtifacts artifacts: 'build\\**', fingerprint: true
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

                echo '============================================'
                echo 'DEPLOYING APPLICATION TO STAGING'
                echo '============================================'

                bat 'if exist staging rmdir /s /q staging'
                bat 'mkdir staging'

                bat 'xcopy build staging /E /I /Y'

                echo 'Starting Streamlit staging application on port 8502...'

                bat 'start "Streamlit-Staging" /B cmd /c "python -m streamlit run staging\\app.py --server.port 8502 --server.address 127.0.0.1 --server.headless true > staging.log 2>&1"'

                echo 'Waiting for staging application to start...'

                bat """powershell -NoProfile -Command "\$ok=\$false; for(\$i=0; \$i -lt 15; \$i++){ try{\$r=Invoke-WebRequest -Uri http://127.0.0.1:8502 -UseBasicParsing -TimeoutSec 3; if(\$r.StatusCode -eq 200){\$ok=\$true; break} } catch{}; Start-Sleep -Seconds 2 }; if(-not \$ok){Write-Host 'STAGING DEPLOYMENT FAILED'; if(Test-Path staging.log){Get-Content staging.log}; exit 1}; Write-Host 'STAGING DEPLOYMENT SUCCESSFUL'\""""
            }
        }

        stage('Release') {
            steps {

                echo '============================================'
                echo 'RELEASING APPLICATION TO PRODUCTION'
                echo '============================================'

                bat 'if exist production rmdir /s /q production'
                bat 'mkdir production'

                bat 'xcopy staging production /E /I /Y'

                echo 'Stopping previous production application if running...'

                bat """powershell -NoProfile -Command "\$connections=Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue; foreach(\$connection in \$connections){Stop-Process -Id \$connection.OwningProcess -Force -ErrorAction SilentlyContinue}" """

                echo 'Starting Streamlit production application on port 8501...'

                bat 'start "Streamlit-Production" /B cmd /c "python -m streamlit run production\\app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true > production.log 2>&1"'

                echo 'Waiting for production application to start...'

                bat """powershell -NoProfile -Command "\$ok=\$false; for(\$i=0; \$i -lt 15; \$i++){ try{\$r=Invoke-WebRequest -Uri http://127.0.0.1:8501 -UseBasicParsing -TimeoutSec 3; if(\$r.StatusCode -eq 200){\$ok=\$true; break} } catch{}; Start-Sleep -Seconds 2 }; if(-not \$ok){Write-Host 'PRODUCTION RELEASE FAILED'; if(Test-Path production.log){Get-Content production.log}; exit 1}; Write-Host 'PRODUCTION RELEASE SUCCESSFUL'\""""

                bat 'if exist release.zip del /f /q release.zip'

                bat 'powershell -NoProfile -Command "Compress-Archive -Path production\\* -DestinationPath release.zip"'

                archiveArtifacts artifacts: 'release.zip', fingerprint: true
            }
        }

        stage('Monitoring') {
            steps {

                echo '============================================'
                echo 'MONITORING PRODUCTION APPLICATION'
                echo '============================================'

                bat """powershell -NoProfile -Command "\$ok=\$false; try{\$r=Invoke-WebRequest -Uri http://127.0.0.1:8501 -UseBasicParsing -TimeoutSec 10; if(\$r.StatusCode -eq 200){\$ok=\$true}} catch{}; if(\$ok){Write-Host 'MONITORING: HEALTHY - Production application is responding.'} else {Write-Host 'ALERT: Production application is NOT responding.'; exit 1}\""""
            }
        }
    }

    post {
        success {
            echo '============================================'
            echo 'PIPELINE COMPLETED SUCCESSFULLY'
            echo 'Build -> Test -> Code Quality -> Security'
            echo '-> Deploy -> Release -> Monitoring'
            echo '============================================'
        }

        failure {
            echo '============================================'
            echo 'PIPELINE FAILED - CHECK THE FAILED STAGE'
            echo '============================================'
        }
    }
}
