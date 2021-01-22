
<template>
   <div class="d-flex flex-column justify-content-center flex-grow-1 flex-fill" id="intro-header">
    <div class="container">
        <div class="row vh-100 justify-content-center">
            <div class="col-md-auto align-self-center">
                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                      <a class="nav-link active" id="home-tab" data-bs-toggle="tab" href="#sign_in_tab" role="tab" aria-controls="sign_in_tab" aria-selected="true">Sign In</a>
                    </li>
                    <li class="nav-item" role="presentation">
                      <a class="nav-link" id="profile-tab" data-bs-toggle="tab" href="#sign_up_tab" role="tab" aria-controls="sign_up_tab" aria-selected="false">Sign Up</a>
                    </li>
                </ul>
                <div class="tab-content" id="myTabContent">
                    <div class="tab-pane show active" id="sign_in_tab" role="tabpanel" aria-labelledby="home-tab">
                        <div class="card text-white" >
                            <div class="card-body">
                                <AjaxForm inline-template v-on:process="auth">
                                    <form id="sign_in_form" @submit.prevent="processForm">
                                        <div class="alert alert-success" v-if="success" role="alert">
                                            Success!
                                        </div>
                                        <div class="alert alert-danger" v-else-if="failed" role="alert">
                                            Failed :(
                                        </div>
                                        <div class="mb-3 position-relative">
                                            <label for="email" class="form-label">Email</label>
                                            <input type="email" :class="(errors['email']) ? 'form-control is-invalid': 'form-control is-valid'"  placeholder="email" id="email" v-model.trim="requestFields['email']"  required>
                                            <div class="invalid-tooltip" v-if="errors['email']">{{errors['email']}}</div>
                                        </div>
                                        <div class="mb-3 position-relative">
                                            <label for="password" class="form-label">Password</label>
                                            <input type="password" :class="(errors['password']) ? 'form-control is-invalid': 'form-control is-valid'" placeholder="password" id="password"  v-model.trim="requestFields['password']" required>
                                            <div class="invalid-tooltip" v-if="errors['password']">{{errors['password']}}</div>
                                        </div>
                                        <div class="form-group">
                                            <input type="submit" value="Login" class="btn btn-light float-right">
                                        </div>
                                    </form>
                                </AjaxForm>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex justify-content-center">
                                    <a href="#">Forgot your password?</a>
                                </div>
                            </div>
                        </div>
                    </div>   

                    <div class="tab-pane" id="sign_up_tab" role="tabpanel" aria-labelledby="profile-tab">
                        <div class="card text-white">
                            <div class="card-body">
                                <AjaxForm inline-template v-on:process="signup">
                                    <form id="sign_up_form" class="needs-validation" @submit.prevent="processForm" novalidate>
                                        <div class="alert alert-success" v-if="success" role="alert">
                                            Success!
                                        </div>
                                        <div class="alert alert-danger" v-else-if="failed" role="alert">
                                            Failed :(
                                        </div>
                                        <div class="mb-3 position-relative">
                                            <label for="imei" class="form-label">Imei</label>
                                            <input type="text" :class="(errors['imei']) ? 'form-control is-invalid': 'form-control is-valid'" placeholder="imei" id="imei"  v-model.trim="requestFields['imei']"  required>
                                            <div class="invalid-tooltip" v-if="errors['imei']">{{errors['imei']}}</div>
                                        </div>
                                        <div class="mb-3 position-relative">
                                            <label for="email2" class="form-label">Email</label>
                                            <input type="email" :class="(errors['email']) ? 'form-control is-invalid': 'form-control is-valid'"  placeholder="email" id="email2" v-model.trim="requestFields['email']" required>
                                            <div class="invalid-tooltip" v-if="errors['email']">{{errors['email']}}</div>
                                        </div>
                                        <div class="mb-3 position-relative">
                                            <label for="password2" class="form-label">Password</label>
                                            <input type="password" :class="(errors['password']) ? 'form-control is-invalid': 'form-control is-valid'" placeholder="password" id="password2" v-model.trim="requestFields['password']" required>
                                            <div class="invalid-tooltip" v-if="errors['password']">{{errors['password']}}</div>
                                        </div>
                                        <div class="mb-3 position-relative">
                                            <label for="password2r" class="form-label">Repeat</label>
                                            <input type="password" :class="(errors['password_confirm']) ? 'form-control is-invalid': 'form-control is-valid'" placeholder="repeat password" id="password2r" v-model.trim="requestFields['password_confirm']" required>
                                            <div class="invalid-tooltip" v-if="errors['password_confirm']">{{errors['password_confirm']}}</div>
                                        </div>

                                        <div class="form-group">
                                            <input type="submit" value="Login" class="btn btn-light float-right">
                                        </div>
                                    </form>
                                </AjaxForm>
                            </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</div>
</div> 
</template>

<style scoped>
    #intro-header {
            background: url('https://source.unsplash.com/twukN12EN7c/1920x1080') no-repeat center center fixed;
            -webkit-background-size: cover;
            -moz-background-size: cover;
            background-size: cover;
            -o-background-size: cover;
            height:100vh;
            padding-top: 65px;
    }

    .card {
        background-color: rgba(0,0,0,0.5) !important;
    }
</style>


<script>
import {API} from '../models';
import AjaxForm from './AjaxForm.vue'

export default {
  name: 'LoginScreen',
  props: {},
  components: {AjaxForm},
  methods: {
    auth: function(params, ok, fail) { 
        let promise = API.signIn({}, params);
        promise.then( (data) => ok(data.data));
        promise.then(() => this.$emit('authorized'));
        promise.catch( (err) => fail(err.response.data));
    },
    signup: function(params, ok, fail) { 
        let promise = API.signUp({}, params);
        promise.then((data) => ok(data.data));
        promise.catch((err) => fail(err.response.data));
    },
  }
}

</script>