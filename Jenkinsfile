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
		stage('build + cov') {
			when {
				branch 'master'
			}
			steps {
				sh "pip install -r requirements.txt"
				sh "pip install radon pylint"
				sh "radon cc --xml api > ccm.xml"
				sh "coverage run -m unittest discover"
				sh "coverage xml -i"
				step([$class: 'CcmPublisher', pattern: '**/ccm.xml'])

				/*
		        publishHTML target: [
		            allowMissing: false,
		            alwaysLinkToLastBuild: false,
		            keepAll: true,
		            reportDir: '.',
		            reportFiles: 'ccm.xml',
		            reportName: 'CC Report'
		        ]
		        // hope this works
				//sh "pylint -f parseable -d I0011,R0801 api | tee pylint.out"
				
				sh 'pylint --disable=W1202 --output-format=parseable --reports=no api | tee pylint.log'
				step([$class : 'WarningsPublisher',
        			parserConfigurations: [[
                        parserName: 'PYLint',
                        pattern   : 'pylint.log'
                  	]],
        			unstableTotalAll: '0',
        			usePreviousBuildAsReference: true
])
				
				step([$class: 'WarningsPublisher',
        			parserConfigurations: [[
                        parserName: 'radon_cc',
                        pattern: 'ccm.xml'
                	]],
        			unstableTotalAll: '0',
        			usePreviousBuildAsReference: true
				])
				*/
			}
			post{
                always{
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
                          		testResults: 'test-reports/results.xml')
				}
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
