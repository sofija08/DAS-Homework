package com.example.project1.service;

import com.example.project1.model.TradeHistoryEntity;
import com.example.project1.model.CorporateEntity;
import com.example.project1.repository.TradeHistoryRepository;
import com.example.project1.repository.CorporateRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
@RequiredArgsConstructor
public class CorporateService {

    private final CorporateRepository corporateRepository;
    private final TradeHistoryRepository tradeHistoryRepository;

    public List<CorporateEntity> findAll() {
        return corporateRepository.findAll();
    }

    public CorporateEntity findById(Long id) throws Exception {
        return corporateRepository.findById(id).orElseThrow(Exception::new);
    }

    public List<TradeHistoryEntity> findAllToday() {
        return tradeHistoryRepository.findAllByDate(LocalDate.now());
    }

}
