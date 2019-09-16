pipeline {
	agent {
		node {
			label 'master'
		}
	}
	options {
		skipDefaultCheckout false
	}
	triggers {
		pollSCM 'H/10 * * * *'
	}
	agent {
		docker {
			image 'python:3'
			args '-u root'
		}
	}
	stages {
		stage('build + cov') {
			when {
				branch 'master'
			}
			steps {
				sh "pip install -r requirements.txt"
				sh "pip install coverage"
				sh "coverage run -m unittest discover"
				sh "coverage xml -i"
				sh "python -m pytest --verbose --junit-xml test-reports/results.xml"
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
			sh "python -m pytest --verbose --junit-xml test-reports/results.xml"
		}
		post {
			always {
				junit 'test-reports/*.xml'
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
	}

}
