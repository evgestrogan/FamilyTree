from typing import List

from tree.models import PartnersMapper, PartnersGet, NodeSchemaGet


def get_partner(partner: PartnersMapper, other_id: str):
    return PartnersGet(partner_id=partner.husband_id if partner.wife_id == other_id else partner.wife_id,
                       wedding_date=partner.wedding_date, divorce_date=partner.divorce_date)


def get_nodes_from_query_result(nodes_with_partners: list) -> List[NodeSchemaGet]:
    nodes = {}
    for item in nodes_with_partners:
        partner = get_partner(item[1], item[0].id) if item[1] else None
        if nodes.get(item[0].id) is None:
            nodes[item[0].id] = NodeSchemaGet(**item[0].__dict__, partners=[partner] if partner else [])
        else:
            if partner:
                nodes[item[0].id].partners.append(partner)
    return list(nodes.values())



