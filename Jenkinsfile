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
		polSCM 'H/10 * * * *'
	}
	stages {
		stage('build + cov') {
			when {
				branch 'master'
			}
			agent {
				docker {
					image 'python:3'
					args '-u root'
				}
			}
			steps {
				sh "pip install coverage"
				sh "python -m coverage xml -o reports/coverage.xml"
			}
		}
		post{
    		always{
        		step([$class: 'CoberturaPublisher',
                   autoUpdateHealth: false,
                   autoUpdateStability: false,
                   coberturaReportFile: 'reports/coverage.xml',
                   failNoReports: false,
                   failUnhealthy: false,
                   failUnstable: false,
                   maxNumberOfBuilds: 10,
                   onlyStable: false,
                   sourceEncoding: 'ASCII',
                   zoomCoverageChart: false])
    	}
		stage('deploy') {
			sh "deploying"
		}
	}
	post {
        failure {
            echo "failed"
            //slackSend (color: 'danger', message: "bumblebee_${GIT_BRANCH} - Build #${BUILD_NUMBER} Failed. (<${env.BUILD_URL}|Open>)")
        }
        success {
        	echo "good"
            //slackSend (color: 'good', message: "bumblebee_${GIT_BRANCH} - Build #${BUILD_NUMBER} Success. (<${env.BUILD_URL}|Open>)")
        }
        always {
            // Docker creates files that is named under root user
            // which jenkins cannot delete due to limited permission.
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
