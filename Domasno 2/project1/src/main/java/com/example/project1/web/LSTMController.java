package com.example.project1.web;

import com.example.project1.service.PricePredictionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class LSTMController {

    private final PricePredictionService PricePredictionService;

    @PostMapping("/predict")
    public ResponseEntity<Double> predictPrice(@RequestParam(name = "companyId") Long companyId) {
        double predictedPrice = PricePredictionService.predictNextMonth(companyId);
        return ResponseEntity.ok(predictedPrice);
    }
}
