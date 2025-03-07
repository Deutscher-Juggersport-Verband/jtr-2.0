import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import {
  AccommodationTypeEnum,
  PricingTypeEnum,
  TournamentFoodEveningEnum,
  TournamentFoodGastroEnum,
  TournamentFoodMorningEnum,
  TournamentFoodNoonEnum,
  TournamentStatus,
} from '@jtr/data-domain/tournament-data';

export interface CreateTournamentRequestBody {
  accommodationCosts?: number;
  accommodationCostsType?: PricingTypeEnum;
  accommodationLocation: string;
  accommodationType: AccommodationTypeEnum;
  additionalInformation: string;
  address: string;
  barefootAllowed: boolean;
  camShoesAllowed: boolean;
  cleatsShoesAllowed: boolean;
  contacts: string[];
  costsText: string;
  deadlines: string;
  depositCosts?: number;
  depositCostsType?: PricingTypeEnum;
  endArrivalDate?: string;
  endDate: string;
  foodEvening: TournamentFoodEveningEnum;
  foodGastro: TournamentFoodGastroEnum;
  foodMorning: TournamentFoodMorningEnum;
  foodNoon: TournamentFoodNoonEnum;
  guestCosts?: number;
  guestCostsType?: PricingTypeEnum;
  houseRulesText: string;
  houseRulesUrl: string;
  location: string;
  name: string;
  pompfCheckText: string;
  pompfCheckUrl: string;
  possibleSpace: number;
  registrationCosts?: number;
  registrationCostsType?: PricingTypeEnum;
  registrationProcedureText: string;
  registrationProcedureType: string;
  registrationStartDate: string;
  schedule: string;
  shoesText: string;
  startArrivalDate?: string;
  startDate: string;
  studdedShoesAllowed: boolean;
  teamId: number;
  tournamentSystemText: string;
  tournamentSystemUrl: string;
}

export interface CreateTournamentResponse {
  tournamentId: number;
}

export interface UpdateTournamentRequestBody {
  tournamentId: number;
  additionalInformation: string;
  name: string;
  startDate: string;
  endDate: string;
  startArrivalDate?: string;
  endArrivalDate?: string;
  address: string;
  possibleSpace: number;
  registrationProcedureType: string;
  registrationProcedureText: string;
  registrationStartDate: string;
  registrationCosts?: number;
  registrationCostsType?: PricingTypeEnum;
  depositCosts?: number;
  depositCostsType?: PricingTypeEnum;
  accommodationCosts?: number;
  accommodationCostsType?: PricingTypeEnum;
  guestCosts?: number;
  guestCostsType?: PricingTypeEnum;
  costsText: string;
  deadlines: string;
  schedule: string;
  contacts: string[];
  accommodationType: AccommodationTypeEnum;
  accommodationLocation: string;
  location: string;
  foodMorning: TournamentFoodMorningEnum;
  foodNoon: TournamentFoodNoonEnum;
  foodEvening: TournamentFoodEveningEnum;
  foodGastro: TournamentFoodGastroEnum;
  tournamentSystemText: string;
  tournamentSystemUrl: string;
  pompfCheckText: string;
  pompfCheckUrl: string;
  houseRulesText: string;
  houseRulesUrl: string;
  studdedShoesAllowed: boolean;
  cleatsShoesAllowed: boolean;
  camShoesAllowed: boolean;
  barefootAllowed: boolean;
  shoesText: string;
}

export interface UpdateTournamentStatusRequestBody {
  tournamentId: number;
  status: TournamentStatus;
}

@Injectable({
  providedIn: 'root',
})
export class TournamentService {
  constructor(private readonly http: HttpClient) {}

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  public create(body: any): Observable<CreateTournamentResponse> {
    const request: CreateTournamentRequestBody = {
      accommodationCosts: body.registration.costs.accommodationCosts,
      accommodationCostsType: body.registration.costs.accommodationCostsType,
      accommodationLocation: body.accommodation.accommodationAddress,
      accommodationType: body.accommodation.accommodationType,
      additionalInformation: body.costsText,
      address: body.basic.address,
      barefootAllowed: body.rules.shoes.barefoot,
      camShoesAllowed: body.rules.shoes.cam,
      cleatsShoesAllowed: body.rules.shoes.cleats,
      contacts: body.contact.contacts,
      costsText: body.registration.costs.costsText,
      deadlines: body.registration.deadlines,
      depositCosts: body.registration.costs.depositCosts,
      depositCostsType: body.registration.costs.depositCostsType,
      endArrivalDate: body.basic.arrivalEndDate,
      endDate: body.basic.tournamentEndDate,
      foodEvening: body.accommodation.food.dinner,
      foodGastro: body.accommodation.food.gastronomy,
      foodMorning: body.accommodation.food.breakfast,
      foodNoon: body.accommodation.food.lunch,
      guestCosts: body.registration.costs.guestCosts,
      guestCostsType: body.registration.costs.guestCostsType,
      houseRulesText: body.rules.houseRules,
      houseRulesUrl: body.rules.houseRulesLink,
      location: 'Keine Angabe',
      name: body.basic.name,
      pompfCheckText: body.rules.pompfCheck,
      pompfCheckUrl: body.rules.pompfCheckLink,
      possibleSpace:
        body.registration.teamCountButton ?? body.registration.teamCountField,
      registrationCosts: body.registration.costs.registrationCosts,
      registrationCostsType: body.registration.costs.registrationCostsType,
      registrationProcedureText: body.registration.registrationProcedureText,
      registrationProcedureType: body.registration.registrationProcedureType,
      registrationStartDate: body.registration.registrationStartDate,
      schedule: body.contact.schedule,
      shoesText: body.rules.shoes.shoesText,
      startArrivalDate: body.basic.arrivalStartDate,
      startDate: body.basic.tournamentStartDate,
      studdedShoesAllowed: body.rules.shoes.studded,
      teamId: body.teamId,
      tournamentSystemText: body.rules.tournamentSystem,
      tournamentSystemUrl: body.rules.tournamentSystemLink,
    };

    return this.http.post<CreateTournamentResponse>(
      '/api/tournament-frontend/create-tournament',
      request
    );
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  public update(tournamentId: number, body: any): Observable<void> {
    const request: UpdateTournamentRequestBody = {
      accommodationCosts: body.registration.costs.accommodationCosts,
      accommodationCostsType: body.registration.costs.accommodationCostsType,
      accommodationLocation: body.accommodation.accommodationAddress,
      accommodationType: body.accommodation.accommodationType,
      additionalInformation: body.costsText,
      address: body.basic.address,
      barefootAllowed: body.rules.shoes.barefoot,
      camShoesAllowed: body.rules.shoes.cam,
      cleatsShoesAllowed: body.rules.shoes.cleats,
      contacts: body.contact.contacts,
      costsText: body.registration.costs.costsText,
      deadlines: body.registration.deadlines,
      depositCosts: body.registration.costs.depositCosts,
      depositCostsType: body.registration.costs.depositCostsType,
      endArrivalDate: body.basic.arrivalEndDate,
      endDate: body.basic.tournamentEndDate,
      foodEvening: body.accommodation.food.dinner,
      foodGastro: body.accommodation.food.gastronomy,
      foodMorning: body.accommodation.food.breakfast,
      foodNoon: body.accommodation.food.lunch,
      guestCosts: body.registration.costs.guestCosts,
      guestCostsType: body.registration.costs.guestCostsType,
      houseRulesText: body.rules.houseRules,
      houseRulesUrl: body.rules.houseRulesLink,
      location: 'Keine Angabe',
      name: body.basic.name,
      pompfCheckText: body.rules.pompfCheck,
      pompfCheckUrl: body.rules.pompfCheckLink,
      possibleSpace:
        body.registration.teamCountButton ?? body.registration.teamCountField,
      registrationCosts: body.registration.costs.registrationCosts,
      registrationCostsType: body.registration.costs.registrationCostsType,
      registrationProcedureText: body.registration.registrationProcedureText,
      registrationProcedureType: body.registration.registrationProcedureType,
      registrationStartDate: body.registration.registrationStartDate,
      schedule: body.contact.schedule,
      shoesText: body.rules.shoes.shoesText,
      startArrivalDate: body.basic.arrivalStartDate,
      startDate: body.basic.tournamentStartDate,
      studdedShoesAllowed: body.rules.shoes.studded,
      tournamentId: tournamentId,
      tournamentSystemText: body.rules.tournamentSystem,
      tournamentSystemUrl: body.rules.tournamentSystemLink,
    };

    return this.http.put<void>('/api/tournament-frontend/update-tournament', request);
  }

  public updateStatus(
    request: UpdateTournamentStatusRequestBody
  ): Observable<void> {
    return this.http.put<void>('/api/tournament-frontend/update-tournament-status', request);
  }
}
