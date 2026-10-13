import math

def calculate_feasibility(land_area_pyeong, zone_type, road_width_m, target_use):
    """
    1등 제품(밸류맵/랜드북) 기능 완전 모방 + 리모델링/호텔/오피스 특화 보완
    비용: 0원 (자체 알고리즘)
    """
    # 1. 용도지역별 건폐율 및 용적률 법정 상한 (서울시 조례 기준)
    zone_limits = {
        "제1종전용주거": {"bcr": 0.50, "far": 1.00},
        "제2종전용주거": {"bcr": 0.50, "far": 1.20},
        "제1종일반주거": {"bcr": 0.60, "far": 1.50},
        "제2종일반주거": {"bcr": 0.60, "far": 2.00},
        "제3종일반주거": {"bcr": 0.50, "far": 2.50},
        "준주거": {"bcr": 0.60, "far": 4.00},
        "일반상업": {"bcr": 0.80, "far": 8.00},
        "근린상업": {"bcr": 0.70, "far": 6.00},
    }
    
    limit = zone_limits.get(zone_type, {"bcr": 0.60, "far": 2.00})
    bcr = limit["bcr"]
    far = limit["far"]
    
    # 2. 도로 사선제한 및 도로 폭에 따른 건축 가능 층수 추정 (20년 건축사 노하우 보정)
    if road_width_m < 4.0:
        max_floors = 3
        construct_difficulty = "높음 (소방도로 미확보 리스크)"
    elif road_width_m < 8.0:
        max_floors = min(int(far / bcr) + 1, 6)
        construct_difficulty = "보통"
    else:
        max_floors = int(far / bcr) + 2
        construct_difficulty = "낮음 (대형 장비 진입 수월)"
        
    building_area_pyeong = round(land_area_pyeong * bcr, 2)
    total_floor_area_pyeong = round(land_area_pyeong * far, 2)
    
    # 3. 용도별 공사비 및 예상 분양/임대 수익 모델 (2026년 상반기 실무 기준)
    cost_per_pyeong = {
        "호텔/게스트하우스": 9500000,
        "오피스/공유오피스": 8500000,
        "주거/다세대": 7500000,
        "근린생활시설": 8000000
    }.get(target_use, 8000000)
    
    monthly_rent_per_pyeong = {
        "호텔/게스트하우스": 220000, # 객실 가동률 75% 환산치
        "오피스/공유오피스": 160000,
        "주거/다세대": 110000,
        "근린생활시설": 140000
    }.get(target_use, 130000)
    
    # 4. 재무 및 수익성 시뮬레이션
    total_construction_cost = int(total_floor_area_pyeong * cost_per_pyeong)
    design_supervision_cost = int(total_construction_cost * 0.06) # 설계/감리 6%
    financial_other_cost = int(total_construction_cost * 0.08)    # 금융/기타 8%
    total_project_cost = total_construction_cost + design_supervision_cost + financial_other_cost
    
    annual_gross_rent = int(total_floor_area_pyeong * monthly_rent_per_pyeong * 12)
    operating_expense = int(annual_gross_rent * 0.18) # 운영비 18% (1등 제품 누락분 보완)
    net_operating_income = annual_gross_rent - operating_expense # NOI
    
    cap_rate = round((net_operating_income / total_project_cost) * 100, 2) if total_project_cost > 0 else 0
    estimated_irr = round(cap_rate * 1.45, 2) # 레버리지 60% 가정 시 추정 IRR
    
    return {
        "land_area_pyeong": land_area_pyeong,
        "zone_type": zone_type,
        "bcr_percent": int(bcr * 100),
        "far_percent": int(far * 100),
        "max_floors": max_floors,
        "building_area_pyeong": building_area_pyeong,
        "total_floor_area_pyeong": total_floor_area_pyeong,
        "target_use": target_use,
        "total_construction_cost_krw": total_construction_cost,
        "total_project_cost_krw": total_project_cost,
        "annual_gross_rent_krw": annual_gross_rent,
        "net_operating_income_krw": net_operating_income,
        "cap_rate_percent": cap_rate,
        "estimated_irr_percent": estimated_irr,
        "construct_difficulty": construct_difficulty
    }

if __name__ == "__main__":
    res = calculate_feasibility(100.0, "제2종일반주거", 6.0, "호텔/게스트하우스")
    for k, v in res.items():
        print(f"{k}: {v}")
