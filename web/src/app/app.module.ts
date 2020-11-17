import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HeaderComponent } from './header/header.component';
import { HomeComponent } from './home/home.component';
import { SensorsComponent } from './sensors/sensors.component';
import { UsersComponent } from './users/users.component';
import { VerifiedSeismsComponent } from './seisms/verified-seisms/verified-seisms.component';
import { UnverifiedSeismsComponent } from './seisms/unverified-seisms/unverified-seisms.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HomeComponent,
    SensorsComponent,
    UsersComponent,
    VerifiedSeismsComponent,
    UnverifiedSeismsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }