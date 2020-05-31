import { Component, OnInit, Input } from '@angular/core';
import {Router, ActivatedRouteSnapshot , Params, ActivatedRoute} from '@angular/router';
import { VerifydoctorService } from '../services/verifydoctor.service';
import * as $ from 'jquery';

// import {ActivatedRouteSnapshot} from ''

export interface IAlert {
  id: number;
  type: string;
  strong?: string;
  message: string;
  icon?: string;
}

@Component({
  selector: 'app-mail-verification',
  templateUrl: './mail-verification.component.html',
  styleUrls: ['./mail-verification.component.css']
})
export class MailVerificationComponent implements OnInit {
  @Input()
  public alerts: Array<IAlert> = [];
  private backup: Array<IAlert>;
  // flag: true;

  constructor(private _router: ActivatedRoute,private doctorService: VerifydoctorService) {
    this.alerts.push({
      id: 1,
      type: 'success',
      strong: 'Success!',
      message: 'This is a success alert—check it out!',
      icon: 'ni ni-like-2'
  }, {
      id: 2, 
      strong: 'Info!',
      type: 'info',
      message: 'This is an info alert—check it out!',
      icon: 'ni ni-bell-55'
  }, {
      id: 3,
      type: 'warning',
      strong: 'Warning!',
      message: 'This is a warning alert—check it out!',
      icon: 'ni ni-bell-55'
  }, {
      id: 4,
      type: 'danger',
      strong: 'Danger!',
      message: 'This is a danger alert—check it out!',
      icon: 'ni ni-support-16'
  });
  this.backup = this.alerts.map((alert: IAlert) => Object.assign({}, alert));
  }
  ngOnInit(): void {
    var id = this._router.snapshot.queryParams['key'];
    var code = this._router.snapshot.queryParams['secret']
    console.log(id,code);
    
    // console.log(id,code)
    // this.doctorService.verifyEmail(id,code).subscribe(res=>{
    //   console.log(res)
    // })
    // console.log(snapshot)
    // console.log(snapshot.queryParams);
    // this._router.queryParams.subscribe((params)=>{
    //   console.log(params)
    // })
    // this.activatedRoute.queryParams.subscribe(params => {
    //   const userId = params['key'];
    //   const code = params['secret']
    //   console.log(userId.url,code);
    // });
  }

  close(alert: IAlert) {
    this.alerts.splice(this.alerts.indexOf(alert), 1);
  }

  // changeFlag(){
  //   this.flag = false
  // }

}
