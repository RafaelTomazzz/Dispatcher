import { UrgencyTypeEnum } from "../enums/urgency-type-enum"

export interface Ticket{
    id: number,
    name: string,
    requesttype_id: string,
    date_creation: Date
    urgency: UrgencyTypeEnum
}



