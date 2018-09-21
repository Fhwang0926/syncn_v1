<template>
  <div class="wrapper">
    <div class="animated fadeIn">
      <b-row>
        <b-col>
          <b-card
            header-tag="header"
            footer-tag="footer">
            <div slot="header">
              <i class="fa fa-align-justify"></i> <strong> Hello! </strong>
              <small>Everyone</small>
            </div>
            <div>
              <b-jumbotron bg-variant="info" text-variant="white" border-variant="dark">
                <template slot="header">
                  Some video in here <br/> ex) youtube
                <hr class="my-4"></template>
                <template slot="header">
                  Sync Sticky Note Free
                </template>
                <template slot="lead">
                  Are you ready for free synchronize to your Windows sticky note 
                </template>
                <hr class="my-4">
                <p>
                  We need Windows Sticky Note synchronize
                  So, We made some code
                </p>
                <b-btn variant="primary" href="#">Do Something</b-btn>
                <b-btn variant="success" href="#">Do Something Else</b-btn>
                <b-btn variant="danger" href="#">Do Something Else</b-btn>
                <b-btn variant="warning" href="#">Do Something Else</b-btn>
              </b-jumbotron>
            </div>
          </b-card>
        </b-col>
      </b-row>
      <!-- <b-row>
        <b-col>
          <b-card
            header-tag="header"
            footer-tag="footer">
            <div slot="header">
              <i class="fa fa-align-justify"></i> <strong> This Team </strong>
            </div>
            <div>
              <b-jumbotron>
                <template slot="header">
                  Bootstrap 4
                </template>
                <template slot="lead">
                  This is a simple hero unit, a simple jumbotron-style component for
                  calling extra attention to featured content or information.
                </template>
                <hr class="my-4">
                <p>
                  It uses utility classes for typography and spacing to space content
                  out within the larger container.
                </p>
                
              </b-jumbotron>
            </div>
          </b-card>
        </b-col>
      </b-row> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'home'
}
</script>

