pipeline {
	agent {
		docker {
			image 'python:3'
			args '-u root'
		}
	}
	options {
		skipDefaultCheckout false
	}
	triggers {
		pollSCM 'H/10 * * * *'
	}
	stages {
		stage('cov + lynt + cc') {
			when {
				branch 'master'
			}
			steps {
				sh "pip install -r requirements.txt"
				sh "pip install radon pylint"
				
				sh "pylint -f parseable -d I0011,R0801,E1101 api | tee pylint.log"

				sh "radon cc --xml api > ccm.xml"
				
				sh "coverage run -m unittest discover"
				sh "coverage xml -i"
				step([$class: 'CcmPublisher', pattern: '**/ccm.xml', reportName: 'CC Report'])

			}
			post{
                always{
			step([$class : 'WarningsPublisher',
				parserConfigurations: [[
				parserName: 'PYLint',
				pattern   : 'pylint.log'
				]],
				// less warnings than this number results in healthy build:
				healthy: '500',
				usePreviousBuildAsReference: true
				])
                    step([$class: 'CoberturaPublisher',
                                   autoUpdateHealth: false,
                                   autoUpdateStability: false,
                                   coberturaReportFile: 'coverage.xml',
                                   failNoReports: false,
                                   failUnhealthy: false,
                                   failUnstable: false,
                                   maxNumberOfBuilds: 10,
                                   onlyStable: false,
                                   sourceEncoding: 'ASCII',
                                   zoomCoverageChart: false])
                }
            }
		}
		stage('test') {
			steps {
				sh "python -m pytest --verbose --junit-xml test-reports/results.xml"
			}
			post {
				always {
					junit (allowEmptyResults: true,
							healthScaleFactor: 0.5,
                          	testResults: 'test-reports/results.xml')
				}
			}
		}
		stage('snyk dependency scan'){
			tools {
       			snyk 'snyk-latest'
        	}
			steps {
		        snykSecurity(
		        	organisation: 'eqx',
		            severity: 'high',
		            snykInstallation: 'snyk-latest',
		            snykTokenId: 'snyk-api-token',

		            targetFile: 'requirements.txt',
		            failOnIssues: 'false'
		        )
			}
		}
	}
	post {
		failure {
            echo "failed"
            //slackSend (color: 'danger', message: "@here jarvis_${BRANCH_NAME} - Build #${BUILD_NUMBER} Failed. (<${env.BUILD_URL}|Open>)")
        }
        success {
            echo "good"
            //slackSend (color: 'good', message: "jarvis_${BRANCH_NAME} - Build #${BUILD_NUMBER} Success. (<${env.BUILD_URL}|Open>)")
        }
        always {
                // Docker creates files that is named under root user
                // which jenkins cannot delete due to limitted permission.
                // Updating all folder permissions so we can do cleanup after every
                // job done.
                echo 'Updating folder permissions.'
                sh "chmod -R 777 ."
            }
        cleanup {
            echo 'Workspace cleanup.'
            deleteDir()
        }
	}
}
