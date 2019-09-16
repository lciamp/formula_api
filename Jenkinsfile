pipeline {
  agent { docker { image 'python:3.6.2 ' } }
  stages {
    stage('build and cov') {
      steps {
        sh 'pip install pytest coverage'
        sh 'pip install -r requirements.txt'
        sh 'python -m coverage xml -o reports/coverage.xml'
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
    stage('test') {
      steps {
        sh 'py.test --junitxml results.xml tests/'
      }   
    }
  }
}
