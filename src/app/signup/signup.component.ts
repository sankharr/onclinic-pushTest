import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { NgForm, FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
    selector: 'app-signup',
    templateUrl: './signup.component.html',
    styleUrls: ['./signup.component.scss'],
    providers: [AuthService]
})
export class SignupComponent implements OnInit {
    test: Date = new Date();
    focus;
    focus1;
    focus2;

    authError: any;

    doctorVal: any = 0;
    user: firebase.User;

    constructor(private auth: AuthService,private router: Router) { }

    ngOnInit() {
        this.auth.eventAuthErrors$.subscribe(data => {  //getting the errors of the fields
            this.authError = data;
        })
        this.auth.getUserState()
            .subscribe(user => {
                this.user = user;
                // console.log(user.displayName);
            })
    }

    createPatient(frm) {
        // console.log("frm function - ",this.user.email);
        if(this.user){                                     
            console.log("at create patient with USER");   //getting registered with google account
            frm.value.email = this.user.email;
            console.log(frm.value);
            this.auth.insertGooglePatientData(frm.value,this.user.uid)
        }
        else{
            console.log("at create patient TS");
            this.auth.createUser(frm.value, "patient")  //getting registerd without google account
        }
        
    }

    createDoctor(frm) {
        // this.auth.createUser(frm.value, "doctor")
        if(this.user){
            console.log("at createDoctor with USER");   //getting registered with google account
            frm.value.email = this.user.email;
            console.log(frm.value);
            this.auth.insertGoogleDoctorData(frm.value,this.user.uid);
            this.router.navigate(['/doctorverification'])
        }
        else{
            console.log("at create patient TS");
            this.auth.createUser(frm.value, "doctor")  //getting registerd without google account
        }
    }
}

// export class userRegForm {
//     name: string;
//     email: string;
//     age: string;
//     telno: string;
//     address: string;
//     password: string
// }
