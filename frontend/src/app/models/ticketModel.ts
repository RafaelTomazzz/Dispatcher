import { UrgencyTypeEnum } from "../enums/urgency-type-enum"

export interface Ticket{
    id: number,
    entities_id: string,
    name: string,
    urgency: UrgencyTypeEnum,
    locations_id: string
    date_creation: Date,
}



