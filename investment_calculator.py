import math
from typing import Dict, List, Tuple
import datetime


class InvestmentCalculator:
    """
    Калькулятор для различных типов инвестиционных расчетов:
    сложный процент, аннуитет, накопления, дивиденды
    """
    
    def __init__(self):
        self.inflation_rate = 0.04  # 4% годовая инфляция по умолчанию
        
    def compound_interest(self, principal: float, annual_rate: float, 
                         years: int, compounds_per_year: int = 12,
                         monthly_contribution: float = 0) -> Dict:
        """
        Расчет сложного процента с возможностью ежемесячных взносов
        
        Формула: A = P(1 + r/n)^(nt) + PMT * [((1 + r/n)^(nt) - 1) / (r/n)]
        """
        rate_per_period = annual_rate / compounds_per_year
        total_periods = years * compounds_per_year
        
        # Рост начального капитала
        future_value_principal = principal * math.pow(
            1 + rate_per_period, 
            total_periods
        )
        
        # Рост регулярных взносов
        if monthly_contribution > 0 and rate_per_period > 0:
            future_value_contributions = monthly_contribution * (
                (math.pow(1 + rate_per_period, total_periods) - 1) / rate_per_period
            )
        else:
            future_value_contributions = monthly_contribution * total_periods
        
        total_future_value = future_value_principal + future_value_contributions
        total_invested = principal + (monthly_contribution * total_periods)
        total_interest = total_future_value - total_invested
        
        # Расчет с учетом инфляции
        real_value = total_future_value / math.pow(1 + self.inflation_rate, years)
        
        return {
            'future_value': total_future_value,
            'total_invested': total_invested,
            'total_interest': total_interest,
            'real_value': real_value,
            'return_percentage': (total_interest / total_invested * 100) if total_invested > 0 else 0,
            'annual_rate': annual_rate * 100,
            'years': years
        }
    
    def calculate_annuity_payment(self, loan_amount: float, annual_rate: float,
                                 years: int, payments_per_year: int = 12) -> Dict:
        """
        Расчет аннуитетного платежа (для кредитов/ипотеки)
        
        Формула: PMT = PV * (r(1+r)^n) / ((1+r)^n - 1)
        """
        rate_per_period = annual_rate / payments_per_year
        total_periods = years * payments_per_year
        
        if rate_per_period == 0:
            payment = loan_amount / total_periods
        else:
            payment = loan_amount * (
                rate_per_period * math.pow(1 + rate_per_period, total_periods)
            ) / (math.pow(1 + rate_per_period, total_periods) - 1)
        
        total_paid = payment * total_periods
        total_interest = total_paid - loan_amount
        
        return {
            'monthly_payment': payment,
            'total_paid': total_paid,
            'total_interest': total_interest,
            'loan_amount': loan_amount,
            'interest_percentage': (total_interest / loan_amount * 100),
            'years': years
        }
    
    def retirement_planning(self, current_age: int, retirement_age: int,
                          current_savings: float, monthly_contribution: float,
                          expected_return: float, desired_monthly_income: float) -> Dict:
        """Планирование пенсионных накоплений"""
        years_to_retirement = retirement_age - current_age
        
        # Накопления к выходу на пенсию
        retirement_savings = self.compound_interest(
            current_savings, 
            expected_return, 
            years_to_retirement,
            12,
            monthly_contribution
        )
        
        # Сколько лет хватит накоплений
        life_expectancy = 85
        retirement_years = life_expectancy - retirement_age
        
        # Необходимый капитал для желаемого дохода
        required_capital = self.calculate_required_capital(
            desired_monthly_income,
            retirement_years,
            expected_return * 0.7  # Консервативная доходность после выхода на пенсию
        )
        
        shortfall = required_capital - retirement_savings['future_value']
        
        # Необходимый ежемесячный взнос для достижения цели
        if shortfall > 0:
            required_monthly = self.calculate_required_monthly_contribution(
                current_savings,
                required_capital,
                expected_return,
                years_to_retirement
            )
        else:
            required_monthly = monthly_contribution
        
        return {
            'current_age': current_age,
            'retirement_age': retirement_age,
            'years_to_retirement': years_to_retirement,
            'current_savings': current_savings,
            'monthly_contribution': monthly_contribution,
            'projected_retirement_savings': retirement_savings['future_value'],
            'required_capital': required_capital,
            'shortfall': shortfall if shortfall > 0 else 0,
            'required_monthly_contribution': required_monthly,
            'desired_monthly_income': desired_monthly_income,
            'retirement_years': retirement_years
        }
    
    def calculate_required_capital(self, monthly_income: float, years: int,
                                  annual_return: float) -> float:
        """Расчет необходимого капитала для желаемого дохода"""
        monthly_rate = annual_return / 12
        total_months = years * 12
        
        if monthly_rate == 0:
            return monthly_income * total_months
        
        # Формула приведенной стоимости аннуитета
        required_capital = monthly_income * (
            (1 - math.pow(1 + monthly_rate, -total_months)) / monthly_rate
        )
        
        return required_capital
    
    def calculate_required_monthly_contribution(self, current_savings: float,
                                               target_amount: float,
                                               annual_return: float,
                                               years: int) -> float:
        """Расчет необходимого ежемесячного взноса для достижения цели"""
        monthly_rate = annual_return / 12
        total_months = years * 12
        
        # Будущая стоимость текущих накоплений
        fv_current = current_savings * math.pow(1 + monthly_rate, total_months)
        
        # Необходимая сумма от регулярных взносов
        needed_from_contributions = target_amount - fv_current
        
        if needed_from_contributions <= 0:
            return 0
        
        if monthly_rate == 0:
            return needed_from_contributions / total_months
        
        # Формула для расчета платежа
        required_payment = needed_from_contributions * monthly_rate / (
            math.pow(1 + monthly_rate, total_months) - 1
        )
        
        return required_payment
    
    def dividend_reinvestment(self, initial_investment: float, 
                            dividend_yield: float, years: int,
                            price_appreciation: float = 0.07) -> Dict:
        """Расчет инвестиций с реинвестированием дивидендов"""
        yearly_data = []
        current_value = initial_investment
        total_dividends = 0
        
        for year in range(1, years + 1):
            # Дивиденды за год
            dividends = current_value * dividend_yield
            total_dividends += dividends
            
            # Реинвестирование дивидендов
            current_value += dividends
            
            # Рост стоимости акций
            current_value *= (1 + price_appreciation)
            
            yearly_data.append({
                'year': year,
                'value': current_value,
                'dividends': dividends
            })
        
        total_return = current_value - initial_investment
        
        return {
            'initial_investment': initial_investment,
            'final_value': current_value,
            'total_dividends': total_dividends,
            'total_return': total_return,
            'return_percentage': (total_return / initial_investment * 100),
            'cagr': self.calculate_cagr(initial_investment, current_value, years),
            'yearly_breakdown': yearly_data
        }
    
    def calculate_cagr(self, beginning_value: float, ending_value: float,
                      years: int) -> float:
        """Расчет среднегодового темпа роста (CAGR)"""
        if years == 0 or beginning_value == 0:
            return 0
        
        cagr = (math.pow(ending_value / beginning_value, 1 / years) - 1) * 100
        return cagr
    
    def dollar_cost_averaging(self, monthly_investment: float, years: int,
                            price_volatility: List[float]) -> Dict:
        """
        Симуляция стратегии усреднения стоимости (DCA)
        price_volatility - список месячных изменений цены в %
        """
        total_invested = 0
        total_shares = 0
        base_price = 100  # Начальная цена за акцию
        
        months = years * 12
        monthly_data = []
        
        for month in range(months):
            # Изменение цены
            if month < len(price_volatility):
                price_change = price_volatility[month]
            else:
                price_change = 0
            
            current_price = base_price * (1 + price_change / 100)
            
            # Покупка акций
            shares_bought = monthly_investment / current_price
            total_shares += shares_bought
            total_invested += monthly_investment
            
            portfolio_value = total_shares * current_price
            
            monthly_data.append({
                'month': month + 1,
                'price': current_price,
                'shares_bought': shares_bought,
                'total_shares': total_shares,
                'invested': total_invested,
                'value': portfolio_value
            })
            
            base_price = current_price
        
        final_value = total_shares * base_price
        total_return = final_value - total_invested
        
        return {
            'total_invested': total_invested,
            'final_value': final_value,
            'total_shares': total_shares,
            'average_price': total_invested / total_shares if total_shares > 0 else 0,
            'total_return': total_return,
            'return_percentage': (total_return / total_invested * 100) if total_invested > 0 else 0,
            'monthly_breakdown': monthly_data
        }
    
    def rule_of_72(self, annual_return: float) -> float:
        """Правило 72 - примерное время удвоения капитала"""
        if annual_return == 0:
            return float('inf')
        return 72 / (annual_return * 100)
    
    def generate_investment_report(self, initial_amount: float, 
                                  monthly_contribution: float,
                                  annual_return: float, years: int) -> str:
        """Генерация подробного инвестиционного отчета"""
        result = self.compound_interest(
            initial_amount, annual_return, years, 12, monthly_contribution
        )
        
        doubling_time = self.rule_of_72(annual_return)
        
        report = []
        report.append("="*70)
        report.append("ИНВЕСТИЦИОННЫЙ ПРОГНОЗ")
        report.append("="*70)
        report.append(f"\nНачальная сумма: {initial_amount:,.2f} ₽")
        report.append(f"Ежемесячный взнос: {monthly_contribution:,.2f} ₽")
        report.append(f"Годовая доходность: {annual_return*100:.2f}%")
        report.append(f"Период инвестирования: {years} лет")
        report.append(f"\nРЕЗУЛЬТАТЫ:")
        report.append(f"Итоговая сумма: {result['future_value']:,.2f} ₽")
        report.append(f"Всего инвестировано: {result['total_invested']:,.2f} ₽")
        report.append(f"Заработано на процентах: {result['total_interest']:,.2f} ₽")
        report.append(f"Доходность: {result['return_percentage']:.2f}%")
        report.append(f"\nС учетом инфляции ({self.inflation_rate*100}%):")
        report.append(f"Реальная стоимость: {result['real_value']:,.2f} ₽")
        report.append(f"\nВремя удвоения капитала: {doubling_time:.1f} лет")
        report.append("="*70)
        
        return "\n".join(report)


# Пример использования
if __name__ == "__main__":
    calc = InvestmentCalculator()
    
    # Расчет сложного процента
    print("=== РАСЧЕТ СЛОЖНОГО ПРОЦЕНТА ===")
    result = calc.compound_interest(
        principal=100000,
        annual_rate=0.12,
        years=10,
        monthly_contribution=5000
    )
    print(calc.generate_investment_report(100000, 5000, 0.12, 10))
    
    # Планирование пенсии
    print("\n=== ПЛАНИРОВАНИЕ ПЕНСИИ ===")
    retirement = calc.retirement_planning(
        current_age=30,
        retirement_age=60,
        current_savings=500000,
        monthly_contribution=15000,
        expected_return=0.10,
        desired_monthly_income=50000
    )
    print(f"Накопления к пенсии: {retirement['projected_retirement_savings']:,.2f} ₽")
    print(f"Необходимо: {retirement['required_monthly_contribution']:,.2f} ₽/месяц")
